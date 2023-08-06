#!/usr/bin/env python

import abc
import time
import typing

# third party
from structlog import get_logger
from dask_sql import Context

# internal
from kurve.entity import Entity
from kurve.sources import PostgresSource, MySQLSource, FileSource
# pydantic models
from kurve.models import EdgeMeta
from kurve.enums import FileProvider


logger = get_logger(__name__)


class EdgeBuilderBase(abc.ABC):
    """
Abstract class for edge builder implementations
    """
    def __init__(self, *args, **kwargs):
        """
Abstract implementation constructor
        """
        pass

    @abc.abstractmethod
    def check_edge_exists (self,
            e1: Entity,
            e2: Entity,
            **kwargs
            ):
        """
Check if an edge exists between two `Entity` instances
        """
        pass


class RelationalSourcePKEdgeBuilder(EdgeBuilderBase):
    """
Implementation for building edges based on a primary key being
present in a child table as a foreign key.
Implemented only for relational data sources.

It is assumed that the source's `get_defined_edges` method
has already been run, which seeds the graph with constraint
edges.
    """
    discovery_mechanism = "pkfk"
    overlap_rate = 0.997
    def __init__ (
            self,
            compute_push_down : bool = True,
            join_limit : int = 100000,
            compute_limit_seconds : float = 120
            ):
        """
Constructor

compute_push_down : bool to tell whether to perform compute on the data source or in memory
join_limit : int to specify a hard limit for the results
compute_limit_seconds : float to specify maximum amount of time to run jobs
        """
        self._push_down = compute_push_down
        self._join_limit = join_limit
        self._compute_limit = compute_limit_seconds

        self._sql_check = """
        SELECT t2.{candidate} as t2_fk, t1.{n.pk} as t1_pk
        FROM {t2} t2
        LEFT JOIN {t1} t1
        ON t2.{candidate} = t1.{n.pk}
        LIMIT {LIMIT}
        """


    def get_pkfk_candidate_cols (
            self,
            e1 : Entity,
            e2 : Entity,
            ) -> typing.Optional[typing.List[tuple]]:
        """
Get the candidate columns for the the pkfk matching
       """
        pk = e1.pk
        if not pk:
            return None
        if not e1.column_type_map:
            e1.load_type_map()
        pk_type = e1.column_type_map[pk]
        candidate_columns = [(c,t) for c, t in e2.column_type_map.items() if t == pk_type and c != e2.pk]
        return candidate_columns


    def check_pkfk_affinity (
            self,
            e1 : Entity,
            e2 : Entity,
            e2fk : str
            ) -> bool:
        """
Check if the candidate column in e2 is a foreign key of e1's primary key 

The join is checking of e2's candidate column joins to e1's primary key
so the check sees how many of e1's primary keys come back non-null from
the LEFT join back to e1 from e2 through e2's candidate foreign key and 
e1's primary key.
        """
        start = time.time()
        cur_limit = 100
        elapsed = time.time() - start
        t1 = '.'.join(e1.identifier.split('.')[1:])
        t2 = '.'.join(e2.identifier.split('.')[1:])
        while cur_limit < self._join_limit and elapsed < self._compute_limit:

            query = self._sql_check.format(
                candidate=e2fk,
                n=e1,
                t2=t2,
                t1=t1,
                LIMIT=cur_limit
            )
            # returns a pd.DataFrame
            result_df = e1.source.run_query(query)
            if not len(result_df):
                return False
            if len(result_df[~result_df['t1_pk'].isnull()])/len(result_df) >= self.overlap_rate:
                elapsed = time.time() - start
                logger.info(f"spent {elapsed} finding pkfk edge")
                return True
            cur_limit *= 10
        return False


    def check_edge_exists (
            self,
            e1 : Entity,
            e2 : Entity
            ) -> typing.Union[EdgeMeta, None]:
        """
Check if the edge exists between e1's primary key and 
e2's available columns.  Since we're doing a comparison 
not just based on names, we'll need data similarity matching
        """

        foreign_keys = []
        candidate_columns = self.get_pkfk_candidate_cols(e1, e2)
        if not candidate_columns:
            return None
        for candidate, _type in candidate_columns:
            affinity = self.check_pkfk_affinity(e1, e2, candidate)
            if affinity:
                foreign_keys.append(candidate)
        if len(foreign_keys) == 1:
            fk = foreign_keys[0]
            edge_meta = EdgeMeta(
                    discovery_mechanism=self.discovery_mechanism,
                    relation_type="child",
                    edge_confidence=None,
                    directed=True,
                    cardinality="1:n",
                    joincols=[(e1.pk, fk)]
                    )
            return edge_meta
        elif len(foreign_keys) > 1:
            #fk = self.filter_final_cols(foreign_keys)

            # if we still have more than 1 fk we need
            # to represent this with multiple join cols
            edge_meta = EdgeMeta(
                    discovery_mechanism=self.discovery_mechanism,
                    relation_type="child",
                    edge_confidence=1.0/len(foreign_keys) if isinstance(foreign_keys, list) else None, 
                    directed=True,
                    cardinality="1:n", 
                    joincols=[e1.pk, fk] if isinstance(foreign_keys, str) else [[e1.pk, _f] for _f in foreign_keys]
                    )  
            return edge_meta
        return None


# for extracting foreign keys from large files
# we need to do the following steps before 
# comparing two tables
# 1) check if the tables are small and, if so, load both tables in their entirety into a dataframe
# 2) if the tables are large, start running iterative joins up to a limit
# 3) extract and repeat

class FileSourcePKEdgeBuilder(EdgeBuilderBase):
    """
Implementation for building edges based on a primary key being present
in a child table as a foreign key.
Implemented only for filesystem sources.
    """

    discovery_mechanism = "pkfk"
    overlap_rate = 0.997 
    def __init__(self, *args, **kwargs):
        """
Constructor
        """
        self._sql_check = """
        SELECT node2.{pkfk} as t2_id, node1.{pk} as t1_id
        FROM node2
        LEFT JOIN node1
        ON node2.{pkfk} = node1.{pk}
        LIMIT {LIMIT}
        """
        super().__init__(*args, **kwargs)
       

    def get_pkfk_candidate_cols (
            self,
            e1 : Entity,
            e2 : Entity,
            ) -> typing.Optional[typing.List[tuple]]:
        """
Get the candidate columns for the the pkfk matching
        """
        pk = e1.pk
        if not pk:
            return None
        if not e1.column_type_map:
            e1.load_type_map()
        pk_type = e1.column_type_map[pk]
        candidate_columns = [(c,t) for c, t in e2.column_type_map.items() if t == pk_type and c != e2.pk]
        return candidate_columns


    def check_pkfk_affinity_join (
            self,
            e1: Entity,
            e2: Entity,
            e2fk : str,
            max_limit : int = 1000000,
            max_time : int = 600,
            compute_layer : str = 'dask'
            ) -> bool:
        """
Using joins, check if the join rate is above the 
`self.overlap_rate`

Define a maximum runtime and maximum limit for
the operation
        """
    
        # start with 100 and work our way up by factors of 10
        start = time.time()
        LIMIT = 1000
        # default to dask if not local
        if e1.source.provider == FileProvider.local and e2.source.provider == FileProvider.local:
            node1df = e1.get_sample()
            node2df = e2.get_sample()
            check = node2df.merge(
                    node1df,
                    left_on=node2df[e2fk],
                    right_on=node1df[e1.pk],
                    suffixes=('', '_right'),
                    how='left'
                    )
            if e1.pk in check.columns:
                if len(check[~check[e1.pk].isnull()])/len(check) >= self.overlap_rate:
                    return True
            elif f"{e1.pk}_right" in check.columns:
                if len(check[~check[f"{e1.pk}_right"].isnull()])/len(check) >= self.overlap_rate:
                    return True
        elif compute_layer == 'dask':
            dask_sql_ctx = Context()
            node1df = e1.get_dask_dataframe()
            node2df = e2.get_dask_dataframe()
            dask_sql_ctx.create_table("node1", node1df)            
            dask_sql_ctx.create_table("node2", node2df)
            query = self._sql_check.format(
                    pkfk=e2fk,
                    pk=e1.pk,
                    LIMIT=LIMIT)
            res = dask_sql_ctx.sql( query )           
            res = res.compute()
            if len(res[~res['t1_id'].isnull()])/len(res) >= self.overlap_rate:
                return True
        elif compute_layer == 'spark':
            spark_ctx = None            
        elif compute_layer == 'pandas':
            pass



    def check_pkfk_affinity (
            self,
            e1 : Entity,
            e2 : Entity,
            e2fk : str
            ) -> bool:
        """
Check if the candidate column in e2 is a foreign key of e1's primary key 

In order for this method to work properly we'll need the entire file
loaded into a dataframe.  Otherwise, we'll have to push this query
down via dask.
        """
        e1samp = e1.get_sample()
        e2samp = e2.get_sample()
        check1 = e2samp[e2fk].isin(e1samp[e1.pk]).sum()/len(e2samp)
        if check1 < self.overlap_rate:
            return False
        elif check1 >= self.overlap_rate:
            check2 = len(e2samp[e2fk].unique())/len(e1samp[e1.pk].unique())
            if check2 >= self.overlap_rate:
                return True
        return False


    def filter_final_cols (
            self,
            e1 : Entity,
            e2 : Entity,
            fks : typing.List[str]
            ) -> str:
        """
If multiple foreign keys were selected, filter to a single one
        """
        for fk in fks:
            if fk.lower().endswith('_id') or fk.lower().endswith('id'):
                return fk
        return fks


    def check_edge_exists (
            self,
            e1 : Entity,
            e2 : Entity
            ) -> typing.Union[EdgeMeta, None]:
        """
Check if the edge exists between e1's primary key and 
e2's available columns.  Since we're doing a comparison 
not just based on names, we'll need data similarity matching
        """
        foreign_keys = []
        candidate_columns = self.get_pkfk_candidate_cols(e1, e2)
        if not candidate_columns:
            return None
        for candidate, _type in candidate_columns:
            affinity = self.check_pkfk_affinity_join(e1, e2, candidate)
            if affinity:
                foreign_keys.append(candidate)
        if len(foreign_keys) == 1:
            fk = foreign_keys[0]
            edge_meta = EdgeMeta(
                    discovery_mechanism=self.discovery_mechanism,
                    relation_type="child",
                    edge_confidence=None,
                    directed=True,
                    cardinality="1:n",
                    joincols=[(e1.pk, fk)]
                    )
            return edge_meta
        elif len(foreign_keys) > 1:
            #fk = self.filter_final_cols(foreign_keys)
            # if we still have more than 1 fk we need
            # to represent this with multiple join cols
            edge_meta = EdgeMeta(
                    discovery_mechanism=self.discovery_mechanism,
                    relation_type="child",
                    edge_confidence=1.0/len(foreign_keys) if isinstance(foreign_keys, list) else None, 
                    directed=True,
                    cardinality="1:n", 
                    joincols=[(e1.pk, fk)] if isinstance(foreign_keys, str) else [(e1.pk, _f) for _f in foreign_keys]
                    )  
            return edge_meta
        return None


class FKConstraintEdgeBuilder(EdgeBuilderBase):
    """
Implementation for building edges based on preexisting and accessible
foreign key constraints from, primarily, relational databases.
    """

    discovery_mechanism = "constraint"       
    def __init__(self, *args, **kwargs):
        """
Constructor
        """
        super().__init__(*args, **kwargs)


    def check_edge_exists (
            self,
            e1 : Entity,
            e2 : Entity
            ) -> typing.Union[EdgeMeta, None]:
        """
Check if we have a foreign key constraint edge available for the two nodes
        """
        logger.info("FKConstraintEdgeBuilder.check_edge_exists")
        pass


class ColnameEdgeBuilder(EdgeBuilderBase):
    discovery_mechanism = "name"
    def __init__(self, *args, **kwargs):
        """
Constructor
        """
        super(ColnameEdgeBuilder, self).__init__(*args, **kwargs)
        self.IGNORE_TYPES = [
                'timestamp',
                'decimal',
                'double',
                'float',
                'float16',
                'float32',                
                'float64',
                'date',
                'date32',
                'date64'
                ]


    def check_edge_exists (
            self,
            e1 : Entity,
            e2 : Entity,
            need_sample : bool = False
            ) -> typing.Union[EdgeMeta, None]:
        """
Check if an edge exists between two `Entity` instances
by analyzing all columns in each entity against the columns
in the other entity instance and looking for nomenclature
similarities
        """
        e1_table = None
        e2_table = None
        e1_fk_name = None
        e2_fk_name = None
        # makes strong assumptions - fk referencing table is `table_name_id`
        if isinstance(e1.source, PostgresSource) or isinstance(e1.source, MySQLSource):
            e1_db, e1_schema, e1_table = e1.identifier.split('.')
            e1_fk_name = f"{e1_table}_id"
            e2_db, e2_schema, e2_table = e2.identifier.split('.')
            e2_fk_name = f"{e2_table}_id"
        elif isinstance(e1.source, FileSource):
            source_format = e1.source.storage_format
            source_provider = e1.source.provider
            e1_parts = e1.identifier.split('/')
            e2_parts = e2.identifier.split('/')
            e1_table = e1_parts[-1].split('.')[0]
            e2_table = e2_parts[-1].split('.')[0]
            e1_fk_name = f"{e1_table}_id"
            e2_fk_name = f"{e2_table}_id"
        else:
            pass

        edge_meta = EdgeMeta(
                discovery_mechanism=self.discovery_mechanism,
                relation_type="child",
                edge_confidence=None,
                directed=True,
                cardinality="1:n",
                joincols=[]
                )
        e2_map = e2.column_type_map
        if not e2_map:
            e2_map = e2.get_type_map()
        e1_map = e2.column_type_map
        if not e1_map:
            e1_map = e1.get_type_map()
        # assumes column in table 1 is `id` and col in table 2 is `tablename_id`
        for c2 in e2.columns:
            # if my primary key is in others
            if c2 == e1_fk_name and 'id' in e1.columns:
                edge_meta.joincols = [("id", c2)]
                return edge_meta 
            elif c2 in e1.columns and c2 == e1.pk and e1.pk.lower() != "id":
                edge_meta.joincols = [(c2, c2)]
                return edge_meta
            # too broad for now
            #elif c2 in e1.columns and e1_map[c2] not in self.IGNORE_TYPES:
            #    edge_meta.joincols = [(c2,c2)]
            #    return edge_meta
        return None



class EmbeddingsEdgeBuilder(EdgeBuilderBase):
    discovery_mechanism = "inference"

    def __init__(self, *args, **kwargs):
        """
Constructor
        """
        super(EmbeddingsEdgeBuilder, self).__init__(*args, **kwargs)


    def check_edge_exists (
            self,
            e1 : Entity,
            e2 : Entity,
            need_sample : bool = True
            ) -> typing.Union[EdgeMeta, None]:
        """
Uses graph embeddings to perform link prediction by embedding similarity
        """

        return None

