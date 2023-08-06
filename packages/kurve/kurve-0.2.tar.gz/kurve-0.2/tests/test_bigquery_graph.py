import time

from google.cloud import bigquery

from entitygraph.graph import EntityGraph
from entitygraph.sources import BigQuerySource


if __name__ == '__main__':
    client = bigquery.client.Client()

    bqs = BigQuerySource(client=client)

    start = time.time()
    graph = EntityGraph(source=bqs)
    graph.build_graph()
    graph.save_graph('big_query_graph.pkl')
    end = time.time()
    print(f"{end-start} to build graph")
    print(f"graph nodes: {len(graph)}")
    print(f"graph edges: {len(graph.edges)}")
