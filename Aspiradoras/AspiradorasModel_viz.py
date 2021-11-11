from AspiradorasModel import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r":0.6}

    if isinstance(agent, VacuumAgent):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0.2
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0.5
        portrayal["r"] = 0.4
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(ModelRoomba,
                       [grid],
                       "Model aspiradoras",
                       {"n": 10,
                        "m": 10,
                        "numAgents": 1,
                        "dirty": 30,
                        "timeLimit":3})
server.port = 8521 # The default
server.launch()

