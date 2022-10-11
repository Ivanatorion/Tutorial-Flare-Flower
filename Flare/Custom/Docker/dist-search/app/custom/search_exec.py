import os.path
import random

from nvflare.apis.dxo import DXO, from_shareable
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal

class LocalSearch(Executor):
    def __init__(
        self,
        data_path="~/data",
        train_task_name="train_task",
        submit_model_task_name="submit_task"
    ):
        super(LocalSearch, self).__init__()
        self._train_task_name = train_task_name
        self._submit_model_task_name = submit_model_task_name

    def create_partition_file(self, file_name, partition_str):
        f = open(file_name, "w")

        for i in range(0, len(partition_str)):
            f.write(str(partition_str[i]) + "\n")

        f.close()

    def create_graph_file(self, file_name, graph_str):
        f = open(file_name, "w")
        f.write(graph_str)
        f.close()

    def run_search(self, graph_file, partition_file, timeout, seed):
        runStr = "./prog --inputFile " + graph_file + " --seed " + str(seed) + " --randomP 0.45 --outputFile result.out --partitionFile " + partition_file + " --timeout " + str(timeout)
        print(runStr)
        os.system(runStr)

    def get_search_result(self):
        pStr = ""
        f = open("result.out", "r")
        file = f.readlines()
        for line in file:
            pStr = pStr + str(line[0])
        f.close()
        return pStr

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        try:
            if task_name == self._train_task_name:
                # Get model weights
                try:
                    dxo = from_shareable(shareable)
                except:
                    self.log_error(fl_ctx, "Unable to extract dxo from shareable.")
                    return make_reply(ReturnCode.BAD_TASK_DATA)

                self.create_graph_file("Graph.txt", dxo.data["graph"])
                self.create_partition_file("Partition.txt", dxo.data["partition"])
                self.run_search("Graph.txt", "Partition.txt", 20, random.randrange(1000))

                if abort_signal.triggered:
                    return make_reply(ReturnCode.TASK_ABORTED)

                outgoing_dxo = DXO(data_kind="Graph", data={"graph" : dxo.data["graph"], "partition" : self.get_search_result()}, meta={})
                return outgoing_dxo.to_shareable()
            elif task_name == self._submit_model_task_name:
                return make_reply(ReturnCode.TASK_UNKNOWN)
            else:
                return make_reply(ReturnCode.TASK_UNKNOWN)
        except:
            self.log_exception(fl_ctx, "Exception.")
            return make_reply(ReturnCode.EXECUTION_EXCEPTION)