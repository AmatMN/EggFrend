from ssd1306 import SSD1306_I2C
from sprite import Sprite
from anim import Anim
from stats import Stats
import time
import framebuf
class EventHandler():

    __isAsleep = False
    __sleepIncTick = 0
    __sleepIncTickLimit = 1000
    __sleepDecTick = 0
    __sleepDecTickLimit = 1000 #650000

    __isEating = False
    __foodDecTick = 0
    __foodDecTickLimit = 1100 #432000
    __eatAnimOrder = [1,2,1,2,3,3,3,4,5,4,5,4,5,4,5,2,1,0]
    __eatAnim = Anim(filename = "momo_eat", x=39, y=16, name = "eat")

    __isWashing = False
    __toiletDecTick = 0
    __toiletDecTickLimit = 1200 #864000
    __dirty = False

    __isHealing = False

    __statusScreenState = False
    __statusScreen = Sprite('stats_menu.pbm', name = "stats")

    __statSheet = None

    @property
    def isAsleep(self)->bool:
        return self.__isAsleep
    
    @property
    def isEating(self)->bool:
        return self.__isEating

    @property
    def statsState(self)->bool:
        return self.__statusScreenState

    @statsState.setter
    def statsState(self, value:bool):
        self.__statusScreenState = value

    def __init__(self, statSheet):
        self.__statSheet = statSheet
        self.__sleepIncTick = time.ticks_ms()
        self.__sleepDecTick = time.ticks_ms()
        self.__foodDecTick = time.ticks_ms()
        self.__toiletDecTick = time.ticks_ms()
    
    def status(self, oled):
        oled.blit(self.__statusScreen.image, 5, 5)

    def fallAsleep(self, value:bool, oled):
        oled.invert(not value)
        self.__isAsleep = value
        if value:
            self.__sleepIncTick = time.ticks_ms()
            print("momo sleep")
        else:
            self.__sleepDecTick = time.ticks_ms()
            print("momo wake")

    def eat(self, oled):
        self.__isEating = True
        self.draw(oled)
        self.__statSheet.hunger += 50
        print("hunger: " + str(self.__statSheet.hunger))
        self.__isEating = False

    def draw(self, oled):
        if self.__isEating:
            for i in self.__eatAnimOrder:
                self.__eatAnim.drawFrame(oled, i)
                oled.show()
                time.sleep(0.25)
            
    def update(self):
        if self.__isAsleep:
            if (time.ticks_ms() - self.__sleepIncTick) > self.__sleepIncTickLimit:
                self.__statSheet.incrementSleep(1)
                self.__sleepIncTick = time.ticks_ms()
        else:
            if (time.ticks_ms() - self.__sleepDecTick) > self.__sleepDecTickLimit:
                self.__statSheet.incrementSleep(-1)
                self.__sleepDecTick = time.ticks_ms()

        if (time.ticks_ms() - self.__foodDecTick) > self.__foodDecTickLimit:
            self.__statSheet.incrementHunger(-1)
            self.__foodDecTick = time.ticks_ms()

        if (time.ticks_ms() - self.__toiletDecTick) > self.__toiletDecTickLimit:
            self.__statSheet.incrementToilet(-1)
            self.__toiletDecTick = time.ticks_ms()
