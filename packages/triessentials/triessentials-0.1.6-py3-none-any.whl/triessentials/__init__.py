__version__ = '0.1.6'

import sys, time, random, os, time

def slowprint(text,delay_time):
 for character in text:      
  sys.stdout.write(character) 
  sys.stdout.flush()
  time.sleep(delay_time)
def random(number1,number2):
 return random.randint(number1,number2)
def clear():
 os.system('clear')
def wait(seconds):
  time.sleep(seconds)
def line():
  print()
 
 
  