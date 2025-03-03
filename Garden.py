import random
from Plant import *

class Event:
    @staticmethod
    def Storm(plants: dict[int, "Plants"]):
        # Simulate a storm event that downgrades the status of each plant
        for plant in plants.values():
            if plant is not None:
                if isinstance(plant.status, str):
                    plant.status = PlantStatus[plant.status]

                if plant.status != PlantStatus.Seed:
                    plant.status = PlantStatus(plant.status.value - 1)
        return plants

    @staticmethod
    def UltimateBonus(plants: dict[int, "Plants"]):
        # Simulate an ultimate bonus event that upgrades the status of each plant
        for plant in plants.values():
            if plant is not None:
                if isinstance(plant.status, str):
                    plant.status = PlantStatus[plant.status]

                if plant.status != PlantStatus.Adult:
                    plant.status = PlantStatus(plant.status.value + 1)

                plant.myWatering = plant.waterRequired[0]
                plant.myfertilizer = plant.fertilizerRequired[0]
                plant.Life = 100
        return plants

    @staticmethod
    def URSSAF(plants: dict[int, "Plants"]):
        # Simulate an URSSAF event that removes all plants
        for index in plants:
            plants[index] = None
        return plants


class Garden:
    PLANT_CLASSES = {"Apple": Apple, "Tomato": Tomato, "WaterMelon": WaterMelon}
    EVENT = ["STORM", "UB", "URSSAF"]

    def __init__(
        self,
        plants: dict[int, Plants] = None,
        event=None,
        day=9,
        isNewGame=False,
        MyWater=10,
        MyFertilizer=1000,
        light=None,
        Money=1000,
        **kwargs,
    ):
        # Initialize the garden with default or provided values
        self.plants = plants if plants is not None else {1: None}
        self.event = event
        self.day = day
        self.IsNewGame = isNewGame
        self.MyWater = MyWater
        self.MyFertilizer = MyFertilizer
        self.light = light if light is not None else random.randint(0, 15000)
        self.MyMoney = Money

    def to_dict(self):
        # Convert the garden state to a dictionary
        return {
            "plants": {
                key: plant.to_dict() if plant else None
                for key, plant in self.plants.items()
            },
            "event": self.event,
            "day": self.day,
            "IsNewGame": self.IsNewGame,
            "MyWater": self.MyWater,
            "MyMoney": self.MyMoney,
            "MyFertilizer": self.MyFertilizer,
            "light": self.light,
        }

    @classmethod
    def from_dict(cls, dictionary: list):
        # Create a garden instance from a dictionary
        plants_data = dictionary.pop("plants", {})
        newplants: dict[int, Plants] = {}
        for plant_id, plant_info in plants_data.items():
            if plants_data[plant_id] != None:
                plant_type = plant_info.pop("type", None)
                plant_class = cls.PLANT_CLASSES.get(plant_type)
                if plant_class: 
                    newplants[int(plant_id)] = plant_class(**plant_info)
        return cls(plants=newplants, **dictionary)

    def Lighting(self, plot, hiding):
        # Set the light exposure for a specific plot
        if plot in self.plants and self.plants[plot] is not None:
            plant = self.plants[plot]
            plant.ishide = hiding
            return {"text": "You allow the plant to grow better", "isError": False}
        return {"text": "No plant here!", "isError": True}

    def Watering(self, plot, amount):
        # Water a specific plot with a given amount
        if plot in self.plants and self.plants[plot] is not None:
            plant = self.plants[plot]
            if self.MyWater >= amount:
                plant.myWatering += amount
                self.MyWater -= amount
                return {
                    "text": f"You dry your plant with {amount}L d'eau.",
                    "isError": False,
                }
            else:
                amount = self.MyWater
                plant.myWatering += amount
                self.MyWater = 0
                return {
                    "text": f"You dry your plant with {amount}L d'eau.",
                    "isError": False,
                }
        return {"text": "No plant here !", "isError": True}

    def Fertilizing(self, plot, amount):
        # Fertilize a specific plot with a given amount
        if plot in self.plants and self.plants[plot] is not None:
            plant = self.plants[plot]
            if self.MyFertilizer >= amount:
                plant.myfertilizer += amount
                self.MyFertilizer -= amount
                return {
                    "text": f"You fertilize with {amount}g.",
                    "isError": False,
                }
            else:
                amount = self.MyFertilizer
                plant.myfertilizer += amount
                self.MyFertilizer = 0
                return {
                    "text": f"You fertilize with {amount}g.",
                    "isError": False,
                }
        return {"text": "No plant here !", "isError": True}

    def RemoveDeadPlant(self):
        # Remove dead plants from the garden
        newplants: dict[int, Plants] = {}
        for index in self.plants:
            if(isinstance(self.plants[index], Plants)):
                self.plants[index].checkRessourceStatus(self)
                if self.plants[index].Life > 0:
                    newplants.update({index: self.plants[index]})
            else :
                newplants.update({index: None})
        self.plants = newplants

    def UpdateAllPlant(self):
        # Update the status of all plants in the garden
        for index in self.plants:
            if(isinstance(self.plants[index], Plants)):
                self.plants[index].RemoveRandRess()

    def GenerateEvent(self, event=""):
        # Generate a random event for the garden
        self.event = event
        if event == "":
            self.event = random.choice(self.EVENT)
        if self.event == "STORM":
            self.plants = Event.Storm(self.plants)
        elif self.event == "UB":
            self.plants = Event.UltimateBonus(self.plants)
        elif self.event == "URSSAF":
            self.plants = Event.URSSAF(self.plants)
            self.MyMoney -= self.MyMoney/2
            
    def SetUpNewDay(self):
        # Set up a new day in the garden
        self.day += 1
        self.light = random.randint(0, 15000)
        self.GenerateEvent() if random.randint(0,10) == 1 else None

    def GenerateMoney(self):
        # Generate money based on the status of the plants
        for index in self.plants:
            if self.plants[index].status == PlantStatus.Adult:
                self.MyMoney += self.plants[index].MoneyValue * random.randint(1, 5)

    def SpendMoney(self, ressourceAdd):
        # Spend money to buy resources or add a plot
        if ressourceAdd == "water":
            if self.MyMoney >= 50:
                self.MyWater += 1
                self.MyMoney -= 50
        elif ressourceAdd == "fertilizer":
            if self.MyMoney >= 25:
                self.MyFertilizer += 50
                self.MyMoney -= 25
        elif ressourceAdd == "plot":
            if self.AddPlot()==False and self.MyMoney >= 150:
                self.MyMoney -= 150

    def AddPlot(self):
        # Add a new plot to the garden
        if len(self.plants) < 15:
            new_plot_id = len(self.plants) + 1
            self.plants[new_plot_id] = None
            return False
        return True
