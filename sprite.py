import framebuf
from machine import Pin
from time import sleep
from os import listdir
import gc

class Sprite():
    with open('backgroundTest.pbm', 'rb') as f:
        f.readline() # magic number
        f.readline() # creator comment
        size = f.readline()
        size = size.split()
        w = int(size[0])
        h = int(size[1])
        data = bytearray(f.read())

    __image = framebuf.FrameBuffer(data, w, h, framebuf.MONO_HLSB)
    __invert = framebuf.FrameBuffer(data, w, h, framebuf.MONO_HLSB)
    for x in range(0, w):
        for y in range(0, h):
            if __invert.pixel(x,y) == 0:
                __invert.pixel(x,y,1)
            else:
                __invert.pixel(x,y,0)
    __x = 0
    __y = 0
    __width = w
    __height = h
    __name = "Empty"

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, buf):
        self.__image = buf
    
    @property
    def x(self)->int:
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value


    @property
    def width(self)->int:
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def y(self)->int:
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def invert(self):
        return self.__invert 

    def __init__(self, filename, x=None, y=None, name=None):
        """ Sets up the default values """
        if name:
            self.__name = name
        if x:
            self.__x = x
        if y:
            self.__y = y
        if filename is not None:
            self.__image = self.loadImg(filename)
            self.__invert = self.loadImg(filename)
        for x in range(0, self.__width):
            for y in range(0, self.__height):
                if self.__invert.pixel(x,y) == 0:
                    self.__invert.pixel(x,y,1)
                else:
                    self.__invert.pixel(x,y,0)

    def loadImg(self, file):
        with open(file, 'rb') as f:
            f.readline() # magic number
            f.readline() # creator comment
            size = f.readline()
            size = size.split()
            self.__width = int(size[0])
            self.__height = int(size[1])
            data = bytearray(f.read())
        fbuf = framebuf.FrameBuffer(data, self.__width, self.__height, framebuf.MONO_HLSB)
        return fbuf
