import copy
from typing import Optional, Dict, List, Tuple, Union

from flwr.server.client_manager import ClientManager
from flwr.server.client_proxy import ClientProxy
from flwr.server.strategy.strategy import Strategy

from flwr.common import (
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    Scalar
)

import Graph as gp

class CustomStrategy(Strategy):
    def __init__(
        self
    ):
        self.config_dict = {
            "gStr" : "",
            "pStr" : "",
            "timeout" : 30,
            #seed...,
            #randomP...,
        }
        
        self.graph = gp.Graph()
        self.partition_value = 0

    def eval_partition(self, partition : str) -> int:
        return self.graph.eval_partition(partition)

    def initialize_parameters(self, client_manager : ClientManager) -> Optional[Parameters]:
        self.config_dict["gStr"] = ""
        self.config_dict["pStr"] = ""
        self.config_dict["timeout"] = 30

        f = open("Graph.txt", "r")
        file = f.readlines()
        for line in file:
            self.config_dict["gStr"] = self.config_dict["gStr"] + line
        f.close()

        f = open("Partition.txt", "r")
        file = f.readlines()
        for line in file:
            self.config_dict["pStr"] = self.config_dict["pStr"] + str(line[0])
        f.close()

        self.graph.load("Graph.txt", "Partition.txt")
        self.partition_value = self.graph.partition_value

        return Parameters([], self.config_dict["pStr"])

    def configure_fit(self, server_round : int, parameters : Parameters, client_manager : ClientManager) -> List[Tuple[ClientProxy, FitIns]]:
        fit_ins = FitIns(parameters, self.config_dict) #Fit Instructions
        clients = client_manager.sample(num_clients=max(client_manager.num_available(), 2), min_num_clients=2)

        result_list = []
        for i in range(0, len(clients)):
            client = clients[i]
            fit_ins_custom = copy.deepcopy(fit_ins)
            fit_ins_custom.config["client_n"] = i + 1

            result_list.append([client, fit_ins_custom])

        return result_list

    def aggregate_fit(self, server_round : int, 
        results: List[Tuple[ClientProxy, FitRes]],
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:

        if (not results):
            return None, {}

        #Update the partition with the best one among the results
        for _, fit_res in results:
            pStr = fit_res.parameters.tensor_type #Workaround
            pValue = self.eval_partition(pStr) 
            if pValue < self.partition_value:
                self.partition_value = pValue
                self.config_dict["pStr"] = pStr
                self.graph.update_partition(pStr)

        return Parameters([], self.config_dict["pStr"]), {}

    #Federated evaluation (not performed here)
    def configure_evaluate(self, server_round : int, parameters : Parameters, client_manager : ClientManager) -> List[Tuple[ClientProxy, EvaluateIns]]:
        return []

    def aggregate_evaluate(self, server_round : int,
        results: List[Tuple[ClientProxy, EvaluateRes]], 
        failures: List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
    ) -> Tuple[Optional[float], Dict[str, Scalar]]:
        return None, {}

    #Server-side evaluate
    def evaluate(self, server_round : int, parameters : Parameters) -> Optional[Tuple[float, Dict[str, Scalar]]]:
        return self.partition_value, {}
