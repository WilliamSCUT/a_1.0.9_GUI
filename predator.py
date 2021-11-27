import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import numpy.linalg as LA
import math
from creature import Creature

class Predator(Creature):
  def __init__(self,starting_pos=[0,0],speed=np.random.randint(15,20),size=np.random.randint(5,10),life = np.random.randint(8,10)):
    super(Predator,self).__init__(starting_pos,speed,size,life)    #调用父类
    self.color = (0,0,0)

  '''
  def eat(self):                  
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
                self.health+=70
                self.fertility+=50
        #self.content=True
      
        else:
            self.moveflag=False