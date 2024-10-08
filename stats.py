import ujson as json

class Stats():
    __sleep = 100
    __sleepMax = 100
    __hunger = 100
    __hungerMax = 100
    __toilet = 100
    __toiletMax = 100
    __health = 100
    __healthMax = 100
    
    @property
    def sleep(self)->int:
        return sleep
    
    @sleep.setter
    def sleep(self, value:int):
        if self.__sleep + value < 0:
            self.__sleep = 0
            self.health = -1
        elif self.__sleep + value > self.__sleepMax:
            self.__sleep = self.__sleepMax
        else:
            self.__sleep += value
        self.saveStats()

    @property
    def hunger(self)->int:
        return hunger
    
    @hunger.setter
    def hunger(self, value:int):
        if self.__hunger + value < 0:
            self.__hunger = 0
            self.health = -1
        elif self.__hunger + value > self.__hungerMax:
            self.__hunger = self.__hungerMax
        else:
            self.__hunger += value
        self.saveStats()

    @property
    def toilet(self)->int:
        return toilet
    
    @toilet.setter
    def toilet(self, value:int):
        if self.__toilet + value < 0:
            self.__toilet = 0
            self.health = -1
        elif self.__toilet + value > self.__toiletMax:
            self.__toilet = self.__toiletMax
        else:
            self.__sleep += value
        self.saveStats()

    @property
    def health(self)->int:
        return health
    
    @health.setter
    def health(self, value:int):
        if self.__health + value < 0:
            self.health = 0
            self.__death()
        elif self.__health + value > self.__healthMax:
            self.__health = self.__healthMax
        else:
            self.__health += value
        self.saveStats()

    def __init__(self):
        try:
            with open('savedata.json', 'r') as f:
                data = json.load(f)
                self.__sleep = data["sleep"]
                self.__hunger = data["hunger"]
                self.__toilet = data["toilet"]
                self.__health = data["health"]
        except:
            self.__sleep = self.__sleepMax
            self.__hunger = self.__hungerMax
            self.__toilet = self.__toiletMax
            self.__health = self.__healthMax
            print("Error loading save file. Stats reset to max")

    def saveStats(self):
        jsonData = {
            "sleep" : self.__sleep,
            "sleepMax" : self.__sleepMax,
            "hunger" : self.__hunger,
            "hungeMax" : self.__hungerMax,
            "toilet" : self.__toilet,
            "toiletMax" : self.__toiletMax,
            "health" : self.__health,
            "healthMax" : self.__healthMax
        }
        try:
            with open('savedata.json', 'w') as f:
                json.dump(jsonData, f)
        except:
            print("Error! Could not save")

    def __death(self):
        self.__sleep = 100
        self.__hunger = 100
        self.__toilet = 100
        self.__health = 100
        self.saveStats()