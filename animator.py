import framebuf
from machine import Pin
from sprite import Sprite
from time import sleep
from os import listdir
import gc

class Anim():
    __frames = []
    __current_frame = 0
    __speed = "normal" # Other speeds are 'fast' and 'slow' - it just adds frames or skips frames
    __speed_value = 0
    __done = False # Has the animation completed
    __loop_count = 0
    __bouncing = False
    __animation_type = "default"
    __pause = 0
    __set = False
    __x = 0
    __y = 0
    __width = 16
    __height = 16
    __cached = False
    __filename = None
    """ other animations types: 
        - loop
        - bounce
        - reverse
    """
    @property
    def set(self)->bool:
        return self.__set

    @set.setter
    def set(self, value:bool)->bool:
        self.__set = value
        if value == True:
            self.load()
        else:
            self.unload()
        return self.__set
            

    @property
    def speed(self):
        """ Returns the current speed """
        return self.__speed

    @speed.setter
    def speed(self, value:str):
        if value in ['very slow','slow','normal','fast']:
            self.__speed = value
            if value == 'very slow':
                self.__pause = 10
                self.__speed_value = 10
            if value == 'slow':
                self.__pause = 1
                self.__speed_value = 1
            if value == "normal":
                self.__pause = 0
                self.__speed_value = 0
        else:
            print(value, "is not a valid value, try 'fast','normal' or 'slow'")

    @property
    def animation_type(self):
        return self.__animation_type

    @animation_type.setter
    def animation_type(self, value):
        if value in ['default','loop','bounce','reverse']:
            self.__animation_type = value
        else:
            print(value," is not a valid Animation type - it should be 'loop','bounce','reverse' or 'default'")

    def __init__(self, frames=None, animation_type:str=None,x:int=None,y:int=None, filename=None):
       """ setup the animation """ 

       if x:
           self.__x = x
       if y:
           self.__y = y 
       self.__current_frame = 0
       if frames is not None:
        self.__frames = frames
       self.__done = False
       self.__loop_count = 1
       if animation_type is not None:
            self.animation_type = animation_type
       if filename:
           self.__filename = filename

    @property
    def filename(self):
        """ Returns the current filename"""
        return self.__filename

    @filename.setter
    def filename(self, value):
        """ Sets the filename """
        self.__filename = value

    def forward(self):
        """ progress the current frame """
        if self.__speed == 'normal':
            self.__current_frame +=1

        if self.__speed in ['very slow','slow']:
            if self.__pause > 0:
                self.__pause -= 1
            else:
                self.__current_frame +=1
                self.__pause = self.__speed_value

        if self.__speed == 'fast':
            if self.__current_frame < self.frame_count +2:
                self.__current_frame +=2
            else:
                self.__current_frame +=1

    def reverse(self):
        if self.__speed == 'normal':
            self.__current_frame -=1

        if self.__speed in ['very slow','slow']:
            if self.__pause > 0:
                self.__pause -= 1
            else:
                self.__current_frame -=1                
                self.__pause = self.__speed_value

        if self.__speed == 'fast':
            if self.__current_frame < self.frame_count +2:
                self.__current_frame -=2
            else:
                self.__current_frame -=1
    
    def load(self):
        """ load the animation files """

        # load the files from disk
        if not self.__cached:
            files = listdir()
            array = []
            for file in files:
                if (file.startswith(self.__filename)) and (file.endswith('.pbm')):
                    s = Sprite(filename=file, x=self.__x, y=self.__y, name=file)
                    # s.invert = True
                    self.__width = s.width
                    self.__height = s.height
                    array.append(s)
            self.__frames = array
            self.__cached = True

    def unload(self):
        """ free up memory """

        self.__frames = None
        self.__cached = False
        gc.collect()

    def animate(self, oled):
        """ Animates the frames based on the animation type and for the number of times specified """

        cf = self.__current_frame # Current Frame number - used to index the frames array
        frame = self.__frames[cf]        
        oled.blit(frame.image, frame.x, frame.y)
       
        if self.__animation_type == "loop":
            # Loop from the first frame to the last, for the number of cycles specificed, and then set done to True
            self.forward()
           
            if self.__current_frame > self.frame_count - 1:
                self.__current_frame = 0
                self.__loop_count -=1
                if self.__loop_count == 0:
                    self.__done = True
            
        if self.__animation_type == "bouncing":
           
            # Loop from the first frame to the last, and then back to the first again, then set done to True
            if self.__bouncing:
               
                if self.__current_frame == 0:
                    if self.__loop_count == 0:
                        self.__done == True
                    else:
                        if self.__loop_count >0:
                            self.__loop_count -=1
                            self.forward()
                            self.__bouncing = False
                    if self.__loop_count == -1:
                        # bounce infinately
                        self.forward()
                        self.__bouncing = False
                if (self.__current_frame < self.frame_count) and (self.__current_frame>0):
                    self.reverse()
            else:
                if self.__current_frame == 0:
                    if self.__loop_count == 0:
                        self.__done == True
                    elif self.__loop_count == -1:
                        # bounce infinatey
                        self.forward()
                    else:
                        self.forward()
                        self.__loop_count -= 1
                elif self.__current_frame == self.frame_count:
                    self.reverse()
                    self.__bouncing = True
                else:
                    self.forward()
            
        if self.__animation_type == "default":
            # loop through from first frame to last, then set done to True
            
            if self.__current_frame == self.frame_count:
                self.__current_frame = 0
                self.__done = True
            else:
                self.forward()
   
    @property
    def frame_count(self):
        """ Returns the total number of frames in the animation """
        return len(self.__frames)
    
    @property
    def done(self):
        """ Has the animation completed """
        if self.__done:
            self.__done = False
            return True
        else:
            return False

    def loop(self, no:int=None):
        """ Loops the animation
        if no is None or -1 the animation will continue looping until animate.stop() is called """

        if no is not None:
            self.__loop_count = no
        else:
            self.__loop_count = -1
        self.__animation_type = "loop"

    def stop(self):
        self.__loop_count = 0
        self.__bouncing = False
        self.__done = True

    def bounce(self, no:int=None):
        """ Loops the animation forwared, then backward, the number of time specified in no,
         if there is no number provided it will animate infinately """

        self.__animation_type = "bouncing"
        if no is not None:
            self.__loop_count = no
        else:
            self.__loop_count = -1

    @property
    def width(self):
        """ Gets the Sprite width """
        return self.__width
    
    @width.setter
    def width(self, value):
        """ Sets the Sprite width """
        self.__width = value
    
    @property
    def height(self):
        """ Gets the Sprite height """
        return self.__width
    
    @height.setter
    def height(self, value):
        """ Sets the Sprite height """
        self.__height = value
