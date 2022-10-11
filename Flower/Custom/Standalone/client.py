import os.path
import random

import flwr as fl

from flwr.common import (
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    GetParametersIns,
    GetParametersRes,
    Status
)

class CustomClient(fl.client.Client):
    def create_partition_file(self, file_name : str, partition_str : str):
        f = open(file_name, "w")

        for i in range(0, len(partition_str)):
            f.write(str(partition_str[i]) + "\n")

        f.close()

    def create_graph_file(self, file_name : str, graph_str : str):
        f = open(file_name, "w")
        f.write(graph_str)
        f.close()

    def run_search(self, graph_file : str, partition_file : str, out_file : str, timeout : int, seed : int):
        runStr = "./prog --inputFile " + graph_file + " --seed " + str(seed) + " --randomP 0.45 --outputFile " + out_file + " --partitionFile " + partition_file + " --timeout " + str(timeout)
        print(runStr)
        os.system(runStr)

    def get_search_result(self, file_name : str) -> str:
        pStr = ""
        f = open(file_name, "r")
        file = f.readlines()
        for line in file:
            pStr = pStr + str(line[0])
        f.close()
        return pStr

    def clear_files(self, f1 : str, f2 : str, f3: str):
        os.remove(f1)
        os.remove(f2)
        os.remove(f3)

    def get_parameters(self, config : GetParametersIns) -> GetParametersRes:
        return GetParametersRes(Status(0, ""), Parameters([], ""))

    def set_parameters(self, parameters : Parameters):
        return

    def fit(self, fit_in : FitIns) -> FitRes:
        client_n = str(fit_in.config["client_n"])

        graph_file = "Graph" + client_n + ".txt"
        partition_file = "Partition" + client_n + ".txt"
        result_file = "result" + client_n + ".out"

        self.create_graph_file(graph_file, fit_in.config["gStr"])
        self.create_partition_file(partition_file, fit_in.config["pStr"])
        self.run_search(graph_file, partition_file, result_file, fit_in.config["timeout"], random.randrange(1000))

        search_result = self.get_search_result(result_file)
        self.clear_files(graph_file, partition_file, result_file)
        return FitRes(Status(0, ""), Parameters([], search_result), 0, {})

    def evaluate(self, parameters : Parameters, config : EvaluateIns) -> EvaluateRes:
        return EvaluateRes(Status(0, ""), 0.0, 0, {})

fl.client.start_client(server_address="[::]:8080", client=CustomClient())