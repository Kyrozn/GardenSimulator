from enum import Enum
import random

class PlantStatus(Enum):
    Seed = 1
    PlantShoot = 2
    Adult = 3


class Plants:
    def __init__(
        self,
        waterRequired: tuple,  # in liters
        fertilizerRequired: tuple,  # in grams
        lightRequired: tuple,  # in lumens
        growSpeed: int,  # in days
        value = 0
    ):
        # Initialize a plant with required resources and growth parameters
        self.waterRequired = waterRequired
        self.fertilizerRequired = fertilizerRequired
        self.lightRequired = lightRequired
        self.growSpeed = growSpeed
        self.myWatering = 0.0
        self.myfertilizer = 0
        self.mygrow = 0
        self.Life = 100
        self.NextCut = growSpeed
        self.status = PlantStatus.Seed
        self.ishide = False
        self.MoneyValue = value

    def to_dict(self):
        # Convert the plant state to a dictionary
        return {
            "type": self.__class__.__name__,
            "waterRequired": self.waterRequired,
            "fertilizerRequired": self.fertilizerRequired,
            "lightRequired": self.lightRequired,
            "growSpeed": self.growSpeed,
            "myWatering": self.myWatering,
            "myfertilizer": self.myfertilizer,
            "mygrow": self.mygrow,
            "Life": self.Life,
            "NextCut": self.NextCut,
            "status": self.status if isinstance(self.status, str) else self.status.name,
            "ishide": self.ishide,
            "MoneyValue": self.MoneyValue
        }

    def Evolve(self):
        # Evolve the plant to the next growth stage
        if self.mygrow >= self.growSpeed:
            if self.status == PlantStatus.Seed:
                self.status = PlantStatus.PlantShoot
                self.growSpeed *= 2
            elif self.status == PlantStatus.PlantShoot:
                self.status = PlantStatus.Adult
        self.mygrow += 1

    def checkRessourceStatus(self, Game):
        # Check and update the plant's resource status
        if (
            self.myWatering < self.waterRequired[0]
            or self.myWatering > self.waterRequired[1]
        ):
            self.Life -= 20
        else:
            self.Life += 5
        if (
            self.myfertilizer < self.fertilizerRequired[0]
            or self.myfertilizer > self.fertilizerRequired[1]
        ):
            self.Life -= 15
        else:
            self.Life += 5
        if Game.light < self.lightRequired[0] or Game.light > self.lightRequired[1]:
            if Game.light > self.lightRequired[1] and self.ishide:
                self.Life += 5
            self.Life -= 5
        else:
            self.Life += 5
        if self.Life > 100:
            self.Life = 100
        self.Evolve()

    def RemoveRandRess(self):
        # Randomly remove some resources from the plant
        self.myWatering -= round(random.uniform(0, self.myWatering), 2)
        self.myfertilizer -= random.randint(0, int(self.myfertilizer))


class Tomato(Plants):
    AdultIcon = "🍅"
    PlantIcon = "🌱"
    SeedIcon = "🫘"

    def __init__(
        self,
        waterRequired=(0.5, 1),
        fertilizerRequired=(15, 50),
        lightRequired=(7000, 1000),
        growSpeed=3,
        value = 5,
        **kwargs,
    ):
        # Initialize a tomato plant with specific parameters
        super().__init__(waterRequired, fertilizerRequired, lightRequired, growSpeed, value)
        self.__dict__.update(kwargs)

    def to_dict(self):
        # Convert the tomato plant state to a dictionary
        base_dict = super().to_dict()
        if base_dict.get("status") == "Seed":
            base_dict.update({"icon": self.SeedIcon})
        elif base_dict.get("status") == "PlantShoot":
            base_dict.update({"icon": self.PlantIcon})
        elif base_dict.get("status") == "Adult":
            base_dict.update({"icon": self.AdultIcon})
        return base_dict


class Apple(Plants):
    AdultIcon = "🌳"
    PlantIcon = "🪵"
    SeedIcon = "🫘"

    def __init__(
        self,
        waterRequired=(3, 4),
        fertilizerRequired=(800, 1200),
        lightRequired=(7000, 1000),
        growSpeed=5,
        value= 10,
        **kwargs,
    ):
        # Initialize an apple plant with specific parameters
        super().__init__(waterRequired, fertilizerRequired, lightRequired, growSpeed, value)
        self.__dict__.update(kwargs)

    def to_dict(self):
        # Convert the apple plant state to a dictionary
        base_dict = super().to_dict()
        if base_dict.get("status") == "Seed":
            base_dict.update({"icon": self.SeedIcon})
        elif base_dict.get("status") == "PlantShoot":
            base_dict.update({"icon": self.PlantIcon})
        elif base_dict.get("status") == "Adult":
            base_dict.update({"icon": self.AdultIcon})
        return base_dict


class WaterMelon(Plants):
    AdultIcon = "🍉"
    PlantIcon = "🌱"
    SeedIcon = "🫘"

    def __init__(
        self,
        waterRequired=(8, 10),
        fertilizerRequired=(20, 40),
        lightRequired=(7000, 13000),
        growSpeed=10,
        value=50,
        **kwargs,
    ):
        # Initialize a watermelon plant with specific parameters
        super().__init__(
            waterRequired, fertilizerRequired, lightRequired, growSpeed, value
        )
        self.__dict__.update(kwargs)

    def to_dict(self):
        # Convert the watermelon plant state to a dictionary
        base_dict = super().to_dict()
        if base_dict.get("status") == "Seed":
            base_dict.update({"icon": self.SeedIcon})
        elif base_dict.get("status") == "PlantShoot":
            base_dict.update({"icon": self.PlantIcon})
        elif base_dict.get("status") == "Adult":
            base_dict.update({"icon": self.AdultIcon})
        return base_dict
