import flwr as fl
import CustomStrategy as cs

fl.server.start_server(config=fl.server.ServerConfig(num_rounds=3), strategy=cs.CustomStrategy())