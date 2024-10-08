import framebuf
from machine import Pin
from sprite import Sprite
from time import sleep
from os import listdir
import gc
import math

class Anim():
    __frames = []
    __currentFrame = 0
    __aType = "default"
    __done = False
    __animDone = False
    __loopCount = 0
    __inverted = False
    __speed = 100
    __maxSpeed = 50
    __pause = 0
    __skipPause = False

    __x = 0
    __y = 0
    __width = 16
    __height = 16
    __filename = None
    __cached = False

    @property
    def frame_count(self):
        return len(self.__frames)
    
    @property
    def currentFrame(self):
        return self.__currentFrame
    
    @currentFrame.setter
    def currentFrame(self, f:int):
        if f < len(self.__frames):
            self.__currentFrame = f
        else:
            print("frame " + str(f) + " does not exist")

    @property
    def aType(self):
        return self.__aType

    @aType.setter
    def aType(self, value):
        if value in ['default','bounce','reverse']:
            self.__aType = value
        else:
            print(value," is not a valid Animation type - it should be 'bounce','reverse' or 'default'")

    @property
    def done(self):
        return self.__animDone

    @property
    def loopCount(self)->int:
        return self.__loopCount

    @loopCount.setter
    def loopCount(self, value:int):
        if value < -1:
            value = -1
        self.__loopCount = value 

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__width

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, value):
        self.__filename = value
    
    @property
    def inverted(self)->bool:
        return self.__inverted
    
    @inverted.setter
    def inverted(self, value:int):
        if value == -1:
            self.__inverted = not self.__inverted
        elif value == 0:
            self.__inverted = False
        elif value == 1:
            self.__inverted = True
        else:
            print("Incorrect value")

    @property
    def speed(self)->float:
        return self.__speed
    
    @speed.setter
    def speed(self, value:float):
        if value > 0 and value <= 1:
            self.__speed = value 
        else:
            print("Incorrect value")

    @property
    def cached(self)->bool:
        return self.__cached

    def __init__(self, aType:str="", x:int=0, y:int=0, filename=None, loops:int=-1):
        if aType is not None:
            self.aType = aType
        if x:
            self.__x = x
        if y:
            self.__y = y
        if filename is not None:
            self.__filename = filename
        if loops < -1:
            loops = -1
        self.__loopCount = loops
        self.load()

    def load(self):
        """ load the animation files """
        if self.__filename is None:
            print("no file name in animation")
            return
        if not self.__cached:
            files = listdir()
            array = []
            for file in files:
                if (file.startswith(self.__filename)) and (file.endswith('.pbm')):
                    s = Sprite(filename=file, x=self.__x, y=self.__y, name=file)
                    self.__width = s.width
                    self.__height = s.height
                    array.append(s)
            self.__frames = array
            self.__cached = True

    def unload(self):
        self.__frames = None
        self.__cached = False
        gc.collect()

    def draw(self, oled):
        if self.__loopCount == 0 and self.__done:
            self.__currentFrame = 0
            self.__animDone = True
            return
        else:
            if self.__animDone:
                self.__skipPause = True
            self.__animDone = False
        
        if self.__loopCount > 0 and self.__done:
            self.__currentFrame = 0
            self.__loopCount -= 1
            self.__done = False
        if self.__loopCount < 0 and self.__done:
            self.__currentFrame = 0
            self.__done = False

        if self.__skipPause:
            self.__skipPause = not self.__skipPause
        else: 
            if self.__pause < math.ceil(self.__maxSpeed * (1 - self.__speed)):
                self.__pause +=1
                return
        
        frame = None
        if self.__aType == 'default':
            frame = self.__default()
        if self.__aType == 'bounce':
            frame = self.__bounce()
        if self.__aType == 'reverse':
            frame = self.__reverse()
        
        if frame is not None:
            oled.blit(frame, self.__x, self.__y)
            self.__pause = 0

    """frame collectors"""
    def __default(self):
        c = self.__currentFrame
        if self.__currentFrame >= len(self.__frames):
            print("error, frame " + str(self.__currentFrame) + " does not exist")

            self.__currentFrame = 0
            self.__done = True
            return
        if self.__currentFrame == len(self.__frames) - 1: 
            self.__currentFrame = 0
            self.__done = True

        if self.__inverted:
            f = self.__frames[c].invert                         
        else:
            f = self.__frames[c].image                          

        self.__currentFrame += 1
        return f

    def __reverse(self):
        c = len(self.__frames) - 1 - self.__currentFrame        
        if c < 0:
            print("error, frame does not exist")
            self.__currentFrame = 0
            self.__done = True
            return
        if c == 0:
            self.__currentFrame = 0
            self.__done = True
        
        if self.__inverted:
            f = self.__frames[c].invert                         
        else:
            f = self.__frames[c].image                          
        
        self.__currentFrame += 1
        return f
    
    def __bounce(self):
        if self.__currentFrame >= (len(self.__frames) * 2) - 2: 
            self.__done = True
            return
        if self.__currentFrame == (len(self.__frames) * 2) - 2: 
            self.__done = True

        if self.__currentFrame < len(self.__frames):            
            if self.__inverted:
                f = self.__frames[self.__currentFrame].invert   
            else:
                f = self.__frames[self.__currentFrame].image    
        elif self.__currentFrame >= len(self.__frames):         
            c = len(self.__frames) - 2 - (self.__currentFrame - len(self.__frames)) 
            if self.__inverted:
                f = self.__frames[c].invert
            else:
                f = self.__frames[c].image
        self.__currentFrame += 1
        return f
        
    def stop(self):
        self.__currentFrame = 0
        self.__animDone = True
        self.__done = True



        
            
    
