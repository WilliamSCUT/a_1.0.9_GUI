'''
Tiger.py
1.Define a subclass of creature,Tiger.
2.Define a specific init function for tiger with different speed,size,life range.
3.Define a eat function to change its health and fertility.
'''

import numpy as np
import random
import numpy.linalg as LA
import math
from creature import Creature

#
class Tiger(Creature):
  # Initialize the tiger when creating it with position,speed,size,life.
  def __init__(self,starting_pos=[0,0],speed=np.random.randint(15,20),size=np.random.randint(5,10),life = np.random.randint(4,6)):
    super(Tiger,self).__init__(starting_pos,speed,size,life)   
    self.color = (0,0,0)
  # Renew the related parameters of tiger after it eat cow or sheep.
  def eat(self):                  
      
    if self.health<100 or self.fertility<70:
        self.health+=50
        self.fertility+=np.random.randint(10,20)
  
    else:
        self.moveflag=False