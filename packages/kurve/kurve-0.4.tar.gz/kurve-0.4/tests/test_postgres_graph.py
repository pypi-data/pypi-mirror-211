#!/usr/bin/env python

import os
import sys
import time

import psycopg2

from entitygraph.graph import EntityGraph
from entitygraph.entity import Entity
from entitygraph.sources import PostgresSource


if __name__ == '__main__':


    con = psycopg2.connect(
        host=os.getenv('fv_prod'),
        user=os.getenv('fv_db_user'),
        password=os.getenv('fv_db_pw'),
        database='fv_prod',
        port=5432
    )

    source = PostgresSource(conn=con,
                           schemas=['public'])

    eg = EntityGraph(source=source)
    print("edge builders:")
    for eb in eg._edge_builders:
        print(eb)
    print("")
    start = time.time()
    eg.build_graph()
    eg.plot_graph(fname='fv_prod_graph.html')
    end = time.time()
    print(f"{end-start} to build graph")
    print(f"graph nodes: {len(eg)}")
    print(f"graph edges: {len(eg.edges())}")

