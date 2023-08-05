__version__ = '0.1.3'

import sys, time, random
from random import randint

def slowprint(text,delay_time):
 for character in text:      
  sys.stdout.write(character) 
  sys.stdout.flush()
  time.sleep(delay_time)
def random(number1,number2):
 return randint(number1,number2)
 
  