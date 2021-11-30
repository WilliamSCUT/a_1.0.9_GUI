'''
Cow.py
1.Define a subclass of creature,Cow.
2.Define a specific init function for cow with different speed,size,life range.
3.Define a eat function to change its health and fertility.
'''
import numpy as np
import random
import numpy.linalg as LA
import math
from creature import Creature

class Cow(Creature):
  # Initialize the cow when creating it with position,speed,size,life.
  def __init__(self,starting_pos=[0,0],speed=np.random.randint(10,15),size=np.random.randint(3,7),life = np.random.randint(3,5)):
    super(Cow,self).__init__(starting_pos,speed,size,life)
    self.color = (255,215,0)    
  # Renew the related parameters of cow after it eat grass.
  def eat(self):                  

    if self.health<100 or self.fertility<70:
        self.health+=50
        self.fertility+=50
  
    else:
        self.moveflag=False