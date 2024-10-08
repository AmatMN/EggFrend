from machine import I2C, Pin, Timer
from ssd1306 import SSD1306_I2C
from sprite import Sprite
from anim import Anim
from button import Button
from toolbar import Toolbar
from stats import Stats
import time
import framebuf
import math

sda = Pin(0)
scl = Pin(1)
id = 0
i2c = I2C(id=id, sda=sda, scl=scl)

oled = SSD1306_I2C(width=128, height=64, i2c=i2c)
oled.init_display()

buttonX = Button(4)
buttonB = Button(3)
buttonA = Button(2)

screenSleep = False
screenSleepTimeLimit = 3600000
screenSleepTimer = 0

oled.invert(1)

sleepIcon = Sprite('sleep_icon.pbm', name = "sleep")
wakeIcon = Sprite('wake_icon.pbm', name = "wake")
feedIcon = Sprite('feed_icon.pbm', name = "feed")

tb = Toolbar(horizontal = 0)
tb.addItem(sleepIcon)
tb.addItem(feedIcon)

idle = Anim(x=39, y=16, filename='momo_idle')
idle.currentFrame = 1
idle.speed = .90

sleep = Anim(x=39, y=16, filename='momo_sleep')
sleep.currentFrame = 1
sleep.speed = .6

statSheet = Stats()


oled.fill_rect(0,0,128,64,0)

screenSleepTimer = time.ticks_ms()

while True:
    """screen sleep test"""
    if ((time.ticks_ms() - screenSleepTimer) > screenSleepTimeLimit):
        if not screenSleep:
            oled.poweroff()
            screenSleep = True
        elif buttonA.is_pressed or buttonB.is_pressed or buttonX.is_pressed:
            oled.poweron()
            screenSleep = False
            screenSleepTimer = time.ticks_ms()
        time.sleep(0.05)
        continue
    else:
        oled.poweron()
        screenSleep = False


    """button test"""
    if buttonA.is_pressed:
        tb.A(oled)
        screenSleepTimer = time.ticks_ms()
    
    if buttonB.is_pressed:
        tb.B(oled)
        screenSleepTimer = time.ticks_ms()

    if buttonX.is_pressed:
        tb.X(oled)
        screenSleepTimer = time.ticks_ms()


    """toolbar test code"""
    if tb.isAsleep:
        if sleep.done:
            oled.invert(0)
            tb.insertItem(toolIn = sleepIcon, toolOut = wakeIcon)
        sleep.draw(oled)
    else:
        if idle.done:
            oled.invert(1)
            tb.insertItem(toolIn = wakeIcon, toolOut = sleepIcon)
        idle.draw(oled)

    oled.blit(feedIcon.image, feedIcon.x, feedIcon.y)

    tb.draw(oled)
    oled.show()
    time.sleep(0.0417)