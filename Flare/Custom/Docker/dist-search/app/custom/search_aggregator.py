from nvflare.apis.dxo import from_shareable
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.aggregator import Aggregator

import Graph as gp

class GraphAggregator(Aggregator):
    def __init__(
        self,
    ):
        self.aggregations = []
        self.graph = gp.Graph()
        self.graph.load("Graph.txt", "Partition.txt")
    
    def graph_value(self, idx : int):
        dxo = from_shareable(self.aggregations[idx])
        return self.graph.eval_partition(dxo.data["partition"])

    def accept(self, shareable: Shareable, fl_ctx: FLContext) -> bool:
        self.aggregations.append(shareable)
        return True

    def aggregate(self, fl_ctx: FLContext) -> Shareable:
        bestIDX = 0
        bestValue = self.graph_value(0)
        print(str(bestValue) + " ", end='')
        for i in range(1, len(self.aggregations)):
            gValue = self.graph_value(i)
            if gValue < bestValue:
                bestIDX = i
                bestValue = gValue
        result = self.aggregations[bestIDX]
        self.aggregations.clear()
        return result