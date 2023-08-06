#!/usr/bin/env python

from entitygraph.enums import GraphComputeLayerEnum


class GraphComputeMiddlewareBase(abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def load_node (
            self,
            n : Entity
            ):
        """
Abstract implementation for loading a node
        """
        pass


    def graph_op (
            self,
            n1 : Entity,
            n2 : Entity
            ):
        """
Abstract implementation for a graph operation
        """
        pass


    def node_op (
            self,
            n : Entity
            ):
        """
Abstract implementation for a node operation
        """
        pass


    def edge_op (
            self,
            n : Entity
            ):
        """
Abstract implementation for an edge operation
        """
        pass



class PandasGraphComputeMiddleware(GraphComputeMiddlewareBase):
    def __init__(self, *args, **kwargs):
        pass


    def graph_op (
            self,
            n1 : Entity,
            n2 : Entity
            ):
        """

        """
