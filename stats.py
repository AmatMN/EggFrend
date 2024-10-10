import ujson as json
import time

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
        return self.__sleep
    
    @sleep.setter
    def sleep(self, value:int):
        if value < 0:
            if self.__sleep > 0:
                print("sleep reached zero at :" + str(time.ticks_ms()))
            self.__sleep = 0
            self.incrementHealth(-2)
        elif value > self.__sleepMax:
            self.__sleep = self.__sleepMax
        else:
            self.__sleep = value
        print("sleep:  " + str(self.__sleep))
        self.saveStats()

    def incrementSleep(self, value:int):
        if self.__sleep + value < 0:
            if self.__sleep > 0:
                print("sleep reached zero at :" + str(time.ticks_ms()))
            self.__sleep = 0
            self.incrementHealth(-2)
        elif self.__sleep + value > self.__sleepMax:
            self.__sleep = self.__sleepMax
        else:
            self.__sleep = self.__sleep + value
        print("sleep:  " + str(self.__sleep))
        self.saveStats()

    @property
    def sleepMax(self)->int:
        return self.__sleepMax

    @property
    def hunger(self)->int:
        return self.__hunger
    
    @hunger.setter
    def hunger(self, value:int):
        if value < 0:
            if self.__hunger > 0:
                print("hunger reached zero at :" + str(time.ticks_ms()))
            self.__hunger = 0
            self.incrementHealth(-3)
        elif value > self.__hungerMax:
            self.__hunger = self.__hungerMax
        else:
            self.__hunger = value
        print("hunger: " + str(self.__hunger))
        self.saveStats()

    def incrementHunger(self, value:int):
        if self.__hunger + value < 0:
            if self.__hunger > 0:
                print("hunger reached zero at :" + str(time.ticks_ms()))
            self.__hunger = 0
            self.incrementHealth(-3)
        elif self.__hunger + value > self.__hungerMax:
            self.__hunger = self.__hungerMax
        else:
            self.__hunger = self.__hunger + value
        print("hunger: " + str(self.__hunger))
        self.saveStats()
    
    @property
    def hungerMax(self)->int:
        return self.__hungerMax

    @property
    def toilet(self)->int:
        return self.__toilet
    
    @toilet.setter
    def toilet(self, value:int):
        if value < 0:
            if self.__toilet > 0:
                print("toilet reached zero at :" + str(time.ticks_ms()))
            self.__toilet = 0
            self.incrementHealth(-1)
        elif value > self.__toiletMax:
            self.__toilet = self.__toiletMax
        else:
            self.__sleep = value
        print("toilet: " + str(self.__toilet))
        self.saveStats()

    def incrementToilet(self, value:int):
        if self.__toilet + value < 0:
            if self.__toilet > 0:
                print("toilet reached zero at :" + str(time.ticks_ms()))
            self.__toilet = 0
            self.incrementHealth(-1)
        elif self.__toilet + value > self.__toiletMax:
            self.__toilet = self.__toiletMax
        else:
            self.__toilet = self.__toilet + value
        print("toilet: " + str(self.__toilet))
        self.saveStats()
    
    @property
    def toiletMax(self)->int:
        return self.__toiletMax

    @property
    def health(self)->int:
        return self.__health
    
    @health.setter
    def health(self, value:int):
        if value < 0:
            if self.__health > 0:
                print("health reached zero at :" + str(time.ticks_ms()))
            self.__health = 0
            # self.__death()
        elif value > self.__healthMax:
            self.__health = self.__healthMax
        else:
            self.__health = value
        self.saveStats()

    def incrementHealth(self, value:int):
        if self.__health + value < 0:
            if self.__health > 0:
                print("health reached zero at :" + str(time.ticks_ms()))
            self.__health = 0
            # self.__death()
        elif self.__health + value > self.__healthMax:
            self.__health = self.__healthMax
        else:
            self.__health = value
        print("toilet: " + str(self.__toilet))
        self.saveStats()

    @property
    def healthMax(self)->int:
        return self.__healthMax

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