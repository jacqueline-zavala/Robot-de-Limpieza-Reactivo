from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

"""
Habitación de MxN espacios.
Número de agentes.
Porcentaje de celdas inicialmente sucias.
Tiempo máximo de ejecución.
"""

class TrashAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        
class VacuumAgent(Agent):
    totalSteps = 0
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        #print(f'I am in new position {new_position}')
        self.model.grid.move_agent(self, new_position)

    def clean(self, agent):
        self.model.grid.remove_agent(agent)
        self.model.clean_cells += 1

    def step(self): 
        # neighbours = self.model.grid.get_neighbors(
        #     self.pos,
        #     moore=True,
        #     include_center=True)
        #x,y = self.pos
        gridContent = self.model.grid.get_cell_list_contents([self.pos])
        #print(f'Mi contenido es {gridContent}')
        trash = False
        trashElement = None
        for element in gridContent:
            #live_neighbours = live_neighbours + element.live
            if isinstance(element, TrashAgent):
                trash = True
                trashElement = element
        if not trash:
            VacuumAgent.totalSteps += 1
            self.move()
        else:
            self.clean(trashElement)

class ModelRoomba(Model):
    def __init__(self, numAgents, m, n, dirty, timeLimit):
        self.grid = MultiGrid(m, n, False)
        self.num_agents = numAgents
        self.tle = timeLimit
        self.stepsTime = 0
        self.dirty_cells = int((dirty * (n*m)) / 100)
        self.clean_cells = (n*m) - self.dirty_cells
        self.schedule = RandomActivation(self)
        self.running = True
        
        for i in range(0,self.num_agents):
            a = VacuumAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

        dirtyCells = set()
        for t in range(self.num_agents+1,self.dirty_cells+self.num_agents):
            b = TrashAgent(t,self)
            self.schedule.add(b)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while (x,y) in dirtyCells:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            dirtyCells.add((x,y))
            self.grid.place_agent(b, (x, y))

    def step(self):
        # self.datacollector.collect(self)
        if(self.clean_cells == 0 or self.tle == self.stepsTime):
            print("Tiempo transcurrido: " + str(self.stepsTime) + ", Número de celdas limpias: " + str(self.clean_cells))
            print(VacuumAgent.totalSteps)
            self.running = False
        else:
            self.stepsTime += 1
            self.schedule.step()