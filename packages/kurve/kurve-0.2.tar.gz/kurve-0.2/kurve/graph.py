#!/usr/bin/env python

# python standard libraries
import json
import pathlib
import traceback
import inspect
import typing
import pickle

# third party libraries
import networkx as nx
import pyvis
from structlog import get_logger

# internal libs
from kurve.cardinality import RelationalCardinality
from kurve.entity import Entity
from kurve.sources import PostgresSource, FileSource, BigQuerySource
from kurve.edge_builder import (
        ColnameEdgeBuilder, 
        EmbeddingsEdgeBuilder, 
        EdgeBuilderBase,
        RelationalSourcePKEdgeBuilder,
        FileSourcePKEdgeBuilder
)
from kurve.models import EdgeMeta

logger = get_logger(__name__)


def check_is_unix_timestamp(samp, c):
    if samp[c].apply(lambda x: 1 if len(str(x)) == 10 else 0).sum() == len(samp):
        return True
    return False


class Graph(nx.DiGraph):
    def __init__(self,
            source,
            name : str = 'kurve'
            ):
        self.source = source
        self._graph_built = False
        # optional datastructure to hold entities from `self.get_entities()`
        self._entities = []

        # implementations for primary key discovery
        self._pk_builders = []

        # implementations for edge discovery
        self._edge_builders = [
                ColnameEdgeBuilder(),
#                RelationalSourcePKEdgeBuilder(),
                FileSourcePKEdgeBuilder()
                ]

        # implementations for cardinality and constraint discovery
        self._meta_discovery = []

        super(Graph, self).__init__()


    def get_entities (
            self, 
            with_samples: bool = False,
            retval : bool = True
            ) -> list:
        """
Accessor method for kurve's source
        """
        logger.info("kurve.get_entities")
        if not self._entities:
            aspec = inspect.getfullargspec(self.source.get_entities)
            if 'with_samples' not in aspec.args:
                self._entities = self.source.get_entities()
            else:
                self._entities = self.source.get_entities(with_samples=with_samples)
        return self._entities


    def populate_nodes (
            self
            ):
        """
Populate the graph's nodes
        """
        entities = self.get_entities()
        for e in entities:
            try:
                e.load_type_map()
            except Exception as e:
                logger.error(f"Encountered an error getting {e.identifier}'s type map")

            if not self.has_node(e):
                self.add_node(e)


    def get_node (
            self,
            identifier : str
            ) -> typing.Optional[Entity]:
        """
Get a node by identifier
        """
        res = [n for n in self.nodes() if n.identifier == identifier]
        if len(res):
            return res[0]
        return None


    def get_entity_samples(self):
        """
Get samples for each of the entities and attach
to the entity instances
        """
        pass

    
    def do_pks(self):
        """
All logic necessary to assign primary keys
        """
        logger.info("kurve.do_pks")
        for ent in self.nodes():
            #TODO:
            #for pk_algorithm in self._pk_builders:
            #    pk_algorithm.find_pk(ent)
            ent.elect_pk()


    def get_defined_pks(self) -> list:
        return self.source.get_defined_pks()


    def get_defined_edges(self) -> list:
        """
Gets predefined edges, which we don't do inference on, we just use
These are things like, in RDBMS world, Foreign Keys
In RDF this would be the predicate https://www.w3.org/TR/rdf-concepts/#dfn-predicate
        """
        logger.debug("kurve.get_defined_edges")
        edges = self.source.get_defined_edges()
        logger.debug(f"Got {len(edges)} defined edges")
        return edges


    def add_edge_builder (
            self,
            builder : EdgeBuilderBase
            ):
        """
Add an edge builder to the graph
        """
        pass


    def add_entity_edge(
            self, 
            node_a : Entity = None,
            node_a_key : str = '',
            node_b : Entity = None,
            node_b_key : str = '',
            from_schema : bool = False
            ):
        """
Add an edge between two entities
        """
        if not self.has_node(node_a):
            self.add_node(node_a)
        if not self.has_node(node_b):
            self.add_node(node_b)            

        if not self.has_edge(node_a, node_b):
            edge_meta = EdgeMeta(
                    discovery_mechanism="constraint",
                    relation_type="child",
                    edge_confidence=1,
                    directed=False,
                    cardinality='1:n',
                    joincols=[(node_a_key, node_b_key)]
                    )
            self.add_edge(node_a, node_b, edge_meta=edge_meta.dict())
        # if we have an edge but from a different key
        elif self.has_edge(node_a, node_b):
            edge_meta = self.get_edge_data(node_a, node_b)
            if (node_a_key, node_b_key) not in edge_meta['edge_meta']['joincols']:
                edge_meta['edge_meta']['joincols'].append((node_a_key, node_b_key))


    def build_graph_relational(self):
        """
Build graph implementation for relational tables
The assumption for schema is:
    database, schema, table

With a database, schema, and table structure we can generate
the entity identifiers with those metadata and apply some
additional edge inference heuristics to build the `kurve`
        """
        entities = self.source.get_entities()
        # add all nodes to the graph if not already added
        if not self._graph_built:
            for ent in entities:
                if not self.has_node(ent):
                    self.add_node(ent)

            # start with already defined edges
            for n1, n2, key1 in self.get_defined_edges():
                self.add_entity_edge(n1, key1, n2, 'id', from_schema=True)

            for node in self.nodes():
                db, schema, table = node.identifier.split('.')
                if table.endswith('s'):
                    # strip the s at the end of the table name (e.g. customers_id becomes customer_id)
                    fkname1 = '{0}_id'.format(table[:-1])
                else:
                    fkname1 = f'{table}_id'
                fkname2 = None
                fkname2 = '_'.join(f'{table}_id'.split('_')[1:]) if len(f'{table}_id'.split('_'))>2 else None
                for node2 in self.nodes():
                    if node != node2:
                        #NOTE: SRI research goes here
                        db2, schema2, table2 = node2.identifier.split('.')
                        for column in node2.columns:
                            if column == fkname1:
                                if not self.has_edge(node, node2):
                                    self.add_entity_edge(node, 'id', node2, column, from_schema=False)
                                # already has an edge
                                elif self.has_edge(node, node2):
                                    edge_data = self[node][node2]
                                    edge_data.update({
                                        f'{node.identifier}_key' : 'id',
                                        f'{node2.identifier}_key' : column,
                                        'from_schema' : False
                                        })
                                    self.add_edge(node, node2, edge_meta=edge_data)
            self._graph_built = True
        pass

    
    def build_graph_relational_new(self):
        """
Build a graph implementation for relational data (postgres, MySQL, Snowflake, etc.)
        """
        logger.info("kurve.build_graph_relational")
        if not self._graph_built:
            self.populate_nodes()
            self.do_pks()
            # get defined edges
            edges_added = 0
            edges_updated = 0
            for edge in self.get_defined_edges():
                const_entity = edge['constraint_entity']
                const_col = edge['constraint_entity_column']
                ref_entity = edge['referenced_entity']
                ref_col = edge['referenced_entity_column']
                if not self.has_edge(ref_entity, const_entity):
                    edge_meta = EdgeMeta(
                            discovery_mechanism="constraint",
                            relation_type="child",
                            directed=False,
                            cardinality="1:n",
                            joincols=[(ref_col, const_col)]
                            )
                    self.add_edge(
                            ref_entity,
                            const_entity,
                            edge_meta=edge_meta.dict()
                            )
                    edges_added += 1
                elif self.has_edge(ref_entity, const_entity):
                    data = self.get_edge_data(ref_entity, const_entity)
                    if (ref_col, const_col) not in data['edge_meta']['joincols']:
                        self[ref_entity][const_entity]['edge_meta']['joincols'].append((ref_col, const_col))
                        edges_updated += 1

            logger.debug(f"Defined edges added: {edges_added} - Edges updated: {edges_updated}")

            for n1 in self.nodes():
                for n2 in self.nodes():
                    #TODO: check for self referencing nodes
                    if n1 == n2:
                        continue
                    else:
                        #TODO: allow for multiedge relations
                        for edge_builder in self._edge_builders:
                            if isinstance(edge_builder, FileSourcePKEdgeBuilder):
                                continue
                            try:
                                edge_meta = edge_builder.check_edge_exists(n1, n2)
                            except Exception as e:
                                logger.error(f"error building edge: {e}")
                                continue

                            if edge_meta:
                                edge_meta = edge_meta.dict()
                                logger.debug(f"Found edge: {edge_meta}")
                                if not self.has_edge(n1, n2):
                                    self.add_edge(n1, n2, edge_meta=edge_meta)
                                elif self.has_edge(n1, n2):
                                    edge_data = self.get_edge_data(n1, n2)
                                    joincols = edge_data['edge_meta']['joincols']
                                    if edge_meta['joincols'][0] not in joincols:
                                        logger.debug(f"Updating edge with additional join cols for a total of {len(edge_data['edge_meta']['joincols'])} sets of columns")
                                        self[n1][n2]['edge_meta']['joincols'].append(edge_meta['joincols'][0])
        self._graph_built = True
        return self._graph_built



    def build_graph_filesystem(self):
        """
Build graph implementation for filesystem (local, s3, blob, gcfs)
The assumption for schema is:

    root path, relative path, filename, and storage format

With these parts parameterized in the dependency `Source` instance
we apply this algorithm
        """
        logger.info("kurve.build_graph_filesystem")
        if not self._graph_built:
            self.populate_nodes()
            self.do_pks()
            for n1 in self.nodes():
                for n2 in self.nodes():
                    # self reference is possible, so this conditional
                    # doesn't necessarily need to be here for self
                    # referential edge building...
                    if n1 == n2:
                        continue
                    else:
                        # should we update the edge metadata
                        # with the additional edge information
                        # if we discover multiple edges?
                        for edge_builder in self._edge_builders:
                            # stop gap measure for now
                            if isinstance(edge_builder, RelationalSourcePKEdgeBuilder):
                                continue
                            edge_meta = edge_builder.check_edge_exists(n1, n2)
                            if edge_meta:
                                edge_meta = edge_meta.dict()
                                logger.debug(f"Found edge: {edge_meta}")
                                if not self.has_edge(n1, n2):
                                    self.add_edge(n1, n2, edge_meta=edge_meta)
                                elif self.has_edge(n1, n2):
                                    edge_data = self.get_edge_data(n1, n2)
                                    joincols = edge_data['edge_meta']['joincols']
                                    if edge_meta['joincols'][0] not in joincols:
                                        self[n1][n2]['edge_meta']['joincols'].append(edge_meta['joincols'][0])

            self._graph_built = True
        pass


    def build_graph_warehouse(self):
        if not self._graph_built:
            self.populate_nodes()
            self.do_pks()
            for n1, n2, key1 in self.get_defined_edges():
                self.add_entity_edge(n1, key1, n2, 'id', from_schema=True)
            for n1 in self.nodes():
                for n2 in self.nodes():
                    if n1 == n2:
                        continue
                    else:
                        if not self.has_edge(n1, n2):
                            for builder in self._edge_builders:
                                edge_meta = None
                                edge_meta = builder.check_edge_exists(n1, n2)
                                if edge_meta:
                                    self.add_edge(n1, n2, edge_meta=edge_meta)
                                    continue


    def build_graph_custom(self):
        pass


    def build_graph(self):
        """
Build the entity graph from our underlying source
        """
        if isinstance(self.source, FileSource):
            self.build_graph_filesystem()
        elif isinstance(self.source, PostgresSource) or isinstance(self.source, BigQuerySource):
            self.build_graph_relational_new()
        else:
            self.build_graph_custom()


    def string_nodes(self):
        """
Turns the nodes into strings for visualization packages like `pyvis`
        """
        Gstring = nx.DiGraph()
        for node in self.nodes():
            centrality = nx.centrality.degree_centrality(self)[node]
            Gstring.add_node(
                    node.identifier,
                    mass=centrality*100,
                    title=node.identifier
                    )
        for edge in self.edges():
            Gstring.add_edge(edge[0].identifier, edge[1].identifier)
        return Gstring


    def plot_graph(self, 
            fname : str = 'entity_graph.html', 
            w : str = '1000px', 
            h : str ='1000px',
            notebook : bool = False,
            directed : bool = False):
        """
Plot an entity graph with `pyvis`

fname: str of path to file name
w : str of width default '500px'
h : str of height default '500px'
        """
        gstring = self.string_nodes()
        nt = pyvis.network.Network(w, h, notebook=notebook, directed=directed, bgcolor="#222222", font_color="white")
        nt.from_nx(gstring)
        nt.show(fname)


    def include_domain_expertise(self):
        """
Iterates through the graph and encodes custom domain expertise
        """
        pass


    def infer_edge(self, n1, n2):
        """
Attempts to infer an edge between two nodes (connected or disconnected) in the graph

This method should wrap other more specific heuristics used to infer edges between nodes
`self.infer_edge_nlp`
`self.infer_edge_dtypes`
`self.infer_edge_composite`
        """
        self.infer_edge_nlp(n1, n2)
        self.infer_edge_dtypes(n1, n2)
        self.infer_edge_composite(n1, n2)


    def infer_edge_nlp(self, n1, n2):
        """
Use NLP approaches to inferring an edge between two entities
        """
        pass


    def infer_edge_dtypes(self, n1, n2):
        """
User datatypes and distributions to infer an edge between two entities
        """
        pass


    def infer_edge_composite(self, n1, n2):
        """
To start we may brute force the problem of inferring edges between entities through composite attributes
        """
        pass


    def infer_cardinality(
            self, 
            n1: Entity, 
            n2: Entity) -> RelationalCardinality:
        """
Attempt to infer the cardinality between two nodes
        """
        # which keys are in the edge to use here?
        pass


    def optimize_paths_distance_hops(start, end):
        """
Something like a Dijkstra's implementation for shortest path

Usage: `optimize_paths_distance_hops(G, 'table1', 'table2')
-> ['table1', 'tableX', 'table2']

Parameters
----------
start : str node to start with
end : str node to end with
Returns
---------
paths : list of paths to take
        """
        nodes_to_traverse = []
        paths = {}
        for n in G.neighbors(start):
            nodes_to_traverse.append( n )
            try:
                paths[n] = {
                        'path' : [start, n],
                        'paths' : []
                        }
            except Exception as e:
                print("Failed on node: {0}".format(n))
        while len(nodes_to_traverse) > 0:
            n = nodes_to_traverse[0]
            del nodes_to_traverse[0]
            for n1 in G.neighbors(n):
                if not paths.get(n1):
                    paths[n1] = {
                        'path' : paths[n]['path'] + [n1],
                        'paths' : [ paths[n]['path'] + [n1] ]
                        }
                    nodes_to_traverse.append(n1)
                else:
                    paths[n1]['paths'].append(paths[n]['path'] + [n1])
                    if len(paths[n1]['path']) >= len(paths[n]['path'] + [n1]):
                        paths[n1]['path'] = paths[n]['path'] + [n1]
        return paths[end]


    def save_graph (
            self,
            fpath : str
            ) -> bool:
        """
Save a graph to a pickled object
        """

        # in the case of a BigQuerySource this will fail
        # without checks for the local client
        if isinstance(self.source, BigQuerySource):
            self.source.client = None
        pickle.dump(self, open(fpath, 'wb'))
        return True


