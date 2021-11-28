import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import numpy.linalg as LA
import math
from creature import Creature

class Sheep(Creature):
  def __init__(self,starting_pos=[0,0],speed=np.random.randint(10,15),size=np.random.randint(3,7),life = np.random.randint(3,5)):
    super(Sheep,self).__init__(starting_pos,speed,size,life)
    self.color = (0,0,250)      #两种不同的颜色
  '''
  def eat(self):
    # print("Sheep has eaten")
    if (self.fertility<100):
      if (self.content==False):
        self.content=True
      else:
        self.moveflag=False
        self.fertility=100
  '''
  def eat(self):                  
        if (self.fertility<100):
      
            if self.health<70 or self.fertility<70:
                self.health+=50
                self.fertility+=50
        #self.content=True
      
        else:
            self.moveflag=False