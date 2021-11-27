import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import numpy.linalg as LA
import math

class Food():
  def __init__(self,pos):
    self.pos = pos
    self.value = 100
    self.size = 2
    self.color = (0,238,0)
    self.eaten = False

  def getPos(self):
    return self.pos 