from abc import ABC

from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.learnable_persistor import LearnablePersistor
import model

class GraphPersistor(LearnablePersistor, ABC):
    def load(self, fl_ctx: FLContext):
        gStr = ""
        pStr = ""

        f = open("Graph.txt", "r")
        file = f.readlines()
        for line in file:
            gStr = gStr + line
        f.close()

        f = open("Partition.txt", "r")
        file = f.readlines()
        for line in file:
            pStr = pStr + str(line[0])
        f.close()

        return model.make_graph_learnable(gStr, pStr)

    def save(self, learnable: model.GraphLearnable, fl_ctx: FLContext):
        f = open("Partition.txt", "w")

        for i in range(0, len(learnable[model.GraphLearnableKey.PARTITION])):
            f.write(learnable[model.GraphLearnableKey.PARTITION][i] + "\n")

        f.close()
        
        return