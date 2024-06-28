# Sznajd Model
from enum import Enum
import networkx as nx
from .model import DiscreteNetworkModel


class Opinion(Enum):
    NEGATIVE = -1
    POSITIVE = 1


class SznajdModel(DiscreteNetworkModel):
    def __init__(self) -> None:
        super.__init__()

    

