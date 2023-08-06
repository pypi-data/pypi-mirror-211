__version__ = '0.1.5'

import sys, time, random, os
from random import randint

def slowprint(text,delay_time):
 for character in text:      
  sys.stdout.write(character) 
  sys.stdout.flush()
  time.sleep(delay_time)
def random(number1,number2):
 return randint(number1,number2)
def clear():
 os.system('clear')
 
  