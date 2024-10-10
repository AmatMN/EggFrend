from sprite import Sprite
from anim import Anim
from eventHandler import EventHandler
import framebuf

class Toolbar():
    """ Models the toolbar """
    __spriteArray = []
    __spacer = 1
    __selectedItem = None
    __selectedIndex = -1
    __isOpen = False
    __horizontal = 0
    __width = 16
    __height = 16
    __framebuf = framebuf.FrameBuffer(bytearray(160*64*1), __width, __height, framebuf.MONO_HLSB)
    __eventHandler = None
    __isAsleep = False

    @property
    def spacer(self):
        return self.__spacer
    
    @spacer.setter
    def spacer(self, value):
        self.__spacer = value

    def __init__(self, eventHandler, spriteArray = [], spacer = 1, horizontal = 0):
        if spriteArray is not None:
            self.__spriteArray = spriteArray
        self.__spacer = spacer
        if horizontal:
            self.__width *= 10
        else:
            self.__height *= 10
        self.__framebuf = framebuf.FrameBuffer(bytearray(160*64*8), self.__width, self.__height, framebuf.MONO_HLSB)
        self.__horizontal = horizontal
        self.__eventHandler = eventHandler

    @property
    def data(self):
        x = 0
        y = 0

        if self.__selectedIndex == -1:
            self.__framebuf = framebuf.FrameBuffer(bytearray(160*64*1), self.__width, self.__height, framebuf.MONO_HLSB)
            return self.__framebuf

        for tool in self.__spriteArray:
            if type(tool) == Sprite:
                f = tool.image
                
                if tool.name == self.selected_item:
                    f = tool.invert
                
                self.__framebuf.blit(f, x, y)
            elif type(tool) == Anim:
                f = tool.__frames[tool.__currentFrame].image
                
                if tool.name == self.selected_item:
                    f = tool.__frames[tool.__currentFrame].invert
                
                self.__framebuf.blit(f, x, y)

            if self.__horizontal:
                x += tool.width + self.__spacer
            else:
                y += tool.height + self.__spacer
        return self.__framebuf
    
    @property
    def selected_item(self)->bool:
        self.__selectedItem = self.__spriteArray[self.__selectedIndex].name
        return self.__selectedItem
    
    @property
    def isOpen(self)->bool:
        return self.__isOpen

    def addItem(self, tool):
        self.__spriteArray.append(tool)
    
    def insertItem(self, toolIn, index):
        self.__spriteArray.insert(index, toolIn)
    
    def remove(self, tool):
        self.__spriteArray.remove(tool)

    def select(self, index, oled):
        self.__isOpen = True
        self.__selectedIndex = index
        self.draw(oled)
    
    def unselect(self, oled):
        self.__isOpen = False
        self.__selectedIndex = -1
        self.draw(oled)

    def draw(self, oled):
        oled.blit(self.data, 0, 0)

    def sleep(self, oled):
        self.__isAsleep = not self.__isAsleep
        self.__eventHandler.fallAsleep(self.__isAsleep, oled)
        if self.__isAsleep:
            self.__spriteArray[self.__selectedIndex].currentFrame = 1
        else:
            self.__spriteArray[self.__selectedIndex].currentFrame = 0

    def A(self, oled):
        i = self.__selectedIndex
        if i >= len(self.__spriteArray) - 1:
            i = -1
        self.unselect(oled)
        self.select(i + 1, oled)

    def B(self, oled):
        if self.selected_item == "stats":
            self.__eventHandler.statsState = not self.__eventHandler.statsState
            if not self.__eventHandler.statsState:
                oled.fill_rect(0,0,128,64,0)
            self.unselect(oled)
        elif self.selected_item == "feed":
            if self.__isAsleep:
                self.sleep(oled)
            if self.__eventHandler.statsState:
                self.__eventHandler.statsState = not self.__eventHandler.statsState
            self.unselect(oled)
            oled.show()
            self.__eventHandler.eat(oled)
        elif self.selected_item == "sleep":
            if self.__eventHandler.statsState:
                self.__eventHandler.statsState = not self.__eventHandler.statsState
            self.sleep(oled)
        self.unselect(oled)

    def X(self, oled):
        self.unselect(oled)