__version__ = '0.1.1'

import sys, time, random

class Functions:
  def slowprint(text,delay_time):
   for character in text:      
    sys.stdout.write(character) 
    sys.stdout.flush()
    time.sleep(delay_time)
  def random(number1,number2):
    random.randint(number1,number2)
  