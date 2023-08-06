#!/usr/bin/env python

import re
import os
import time

from entitygraph.sources import FileSource
from entitygraph.enums import FileProvider, StorageFormat
from entitygraph.graph import EntityGraph

if __name__ == '__main__':

    efs = FileSource(
            path_root=os.path.join('/'.join(os.path.abspath(__file__).split('/')[:-1]), 'data'),
            provider=FileProvider.local,
            storage_format=StorageFormat.csv,
            entities_are_partitioned=False
    )

    eg = EntityGraph(source=efs)

    start = time.time()
    eg.build_graph()
    eg.plot_graph(fname='local_filesystem_graph.html')
    end = time.time()
    print(f"{end-start} to build graph")
    print(f"graph nodes: {len(eg)}")
    print(f"graph edges: {len(eg.edges())}")

