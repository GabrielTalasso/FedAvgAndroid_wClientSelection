from Client.client import FedClient
from Server.server_DEEV import FedServer
from Server.server_FedAvgAndroid import FedAvgAndroid
import pickle
import flwr as fl
import os

try:
	os.remove('./results/history_simulation.pickle')
except FileNotFoundError:
	pass

n_clients = 10
n_rounds = 5

def funcao_cliente(cid):
	return FedClient(cid = int(cid), n_clients=n_clients, epochs=1, 
				 model_name            = 'DNN', 
				 client_selection      = True, 
				 solution_name         = 'POC', 
				 aggregation_method    = 'POC',
				 dataset               = 'MNIST',
				 perc_of_clients       = 0.10,
				 decay                 = 0.1,
				 transmittion_threshold = 0.2)

history = fl.simulation.start_simulation(client_fn=funcao_cliente, 
								num_clients=n_clients, 
								strategy=FedServer(aggregation_method='POC',
			    									fraction_fit = 1,
													num_clients = n_clients, 
					                                decay=0.1, 
													perc_of_clients=0.10, 
													dataset='MNIST', 
													solution_name='POC', 
													model_name='DNN'),
								#strategy = FedAvgAndroid(fraction_fit = 1,
				 				#	min_fit_clients = 2,
        						#	min_evaluate_clients = 2,
        						#	min_available_clients= 2),
								
								config=fl.server.ServerConfig(n_rounds))



#with open('./results/history_simulation.pickle', 'wb') as file:
#    pickle.dump(history, file, protocol=pickle.HIGHEST_PROTOCOL)