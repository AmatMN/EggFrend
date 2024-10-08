from machine import Pin
import time

class Button():
    """ Models a button, check the status with is_pressed """

    # The private variables
    __pressed = False
    __pin = 0
    __debounceTime = 0

    def __init__(self, pin:int):
        """ Sets up the button """

        def callback(pin):
            if (time.ticks_ms() - self.__debounceTime) > 300:
                self.__pressed = True
                self.__debounceTime = time.ticks_ms()

        self.__pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.__pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)
        self.__pressed = False


    @property
    def is_pressed(self)->bool:
        """ Returns the current state of the button """

        if not self.__pressed:
            return False
        if self.__pressed:
            self.__pressed = False
            return True
