from nvflare.apis.dxo import DXO
from nvflare.app_common.abstract.learnable import Learnable as GraphLearnable

class GraphLearnableKey(object):
    GRAPH = "graph"
    PARTITION = "partition"

def make_graph_learnable(graph, partition) -> GraphLearnable:
    gl = GraphLearnable()
    gl[GraphLearnableKey.GRAPH] = graph
    gl[GraphLearnableKey.PARTITION] = partition
    return gl

def graph_learnable_to_dxo(gl: GraphLearnable) -> DXO:
    return DXO(data_kind="Graph", data={GraphLearnableKey.GRAPH : gl[GraphLearnableKey.GRAPH], GraphLearnableKey.PARTITION : gl[GraphLearnableKey.PARTITION]}, meta={})