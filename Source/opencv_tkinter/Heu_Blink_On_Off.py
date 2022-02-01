from phue import Bridge
import random
import time, threading

b = Bridge('192.168.2.36')

# Get a flat list of the light objects
lights_list = b.get_light_objects('list')

def blink():
  for light in lights_list:
      light.on = True
      light.bri = 254
      light.xy = [random.random(), random.random()]


def off():
  for light in lights_list:
    light.on = False

for  x in range(0, 1000):
  blink()
  t1 = random.random()
  time.sleep(t1*10)
  off()
  t1 = random.random()
  time.sleep(t1*10)