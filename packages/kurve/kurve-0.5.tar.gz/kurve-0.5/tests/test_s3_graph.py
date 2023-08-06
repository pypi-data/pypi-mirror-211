#!/usr/bin/env python

import re
import time

from entitygraph.sources import FileSource
from entitygraph.enums import FileProvider, StorageFormat
from entitygraph.graph import EntityGraph

if __name__ == '__main__':

    efs = FileSource(
        path_root='prod.emr.freightverify',
        provider=FileProvider.s3,
        storage_format=StorageFormat.parquet,
        prefix='tasks/etl',
        regex_filter=re.compile(r"([a-fA-F\d]{32})"),
        entities_are_partitioned=True
    )


    eg = EntityGraph(source=efs)

    start = time.time()
    eg.build_graph()
    eg.plot_graph('s3_graph.html')
    eg.save_graph('s3_graph.pkl')
    end = time.time()
    print(f"{end-start} to build graph")
    print(f"graph nodes: {len(eg)}")
    print(f"graph edges: {len(eg.edges())}")

