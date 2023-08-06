#!/usr/bin/env python

# standard lib
import typing

# third party
from pydantic import BaseModel, validator



class EdgeMeta (BaseModel):
    """
EntityGraph edge metadata
    """
    discovery_mechanism : str
    relation_type : str
    edge_confidence : typing.Optional[float]
    directed : bool
    cardinality : str
    # [ ('col1', 'col2') ... ]
    joincols : list
