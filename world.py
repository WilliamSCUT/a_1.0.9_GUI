'''
world.py
1.Define the basic class which is called World.
2.Define the initial parameters like world size, sub-regions size.
3.Create data storage container like dictionaries, array.
4.Define six functions related to the operation of the world.
5.Define two functions related to the display of the world.

'''
import torch
import pygame
from pygame import *
import numpy as np
import random
import numpy.linalg as LA
import math
from Tiger import Tiger
from Cow import Cow
from Sheep import Sheep
from food import Food
from evoluation.prey_nn import Prey_nn
from evoluation.predator_nn import Predator_nn


class World():
  # Initialize the world when creating it.
  def __init__(self):
    self.x_range = 600
    self.y_range = 600
    self.numBlocksx=50
    self.numBlocksy=50
    self.blocksize=np.array([self.x_range//self.numBlocksx,self.y_range//self.numBlocksy])
    self.tiger_d = {}
    self.cow_d = {}
    self.dist = 999
    self.target_food = Food([0,0])
    self.target_food_pos = []
    self.sheep_d = {}
    self.target_prey = Cow([0,0])
    self.target_prey_pos = []
    self.food_d = {}
    self.climate = 0
    start=0
    for i in range(51):
        for j in range(51):
            name = 'self.cow_'+str(i)+'_'+str(j)
            exec(name+'={}')
            name = 'self.sheep_'+str(i)+'_'+str(j)
            exec(name+'={}')
            name_p= 'self.tiger_'+str(i)+'_'+str(j)
            exec(name_p+'={}')
            name_f= 'self.food_'+str(i)+'_'+str(j)
            exec(name_f+'={}')


  # Generate corresponding creatures in the world according to user input parameters.
  def initialize_creatures(self, number_of_cow,number_of_sheep,number_of_tiger):
    for i in range(0, number_of_cow):
      new_cow = Cow([random.uniform(0,self.x_range),random.uniform(0,self.y_range)])    
      pos = new_cow.getPos()
      exec('self.cow_'+str(pos[0]//self.blocksize[0])+'_'+str(pos[1]//self.blocksize[1])+'[new_cow]=pos')
      self.cow_d[new_cow] = pos

    for i in range(0, number_of_sheep):
      new_sheep = Sheep([random.uniform(0,self.x_range),random.uniform(0,self.y_range)])    
      pos = new_sheep.getPos()
      exec('self.sheep_'+str(pos[0]//self.blocksize[0])+'_'+str(pos[1]//self.blocksize[1])+'[new_sheep]=pos')
      self.sheep_d[new_sheep] = pos

    for i in range(0, number_of_tiger):
      x = random.uniform(0,self.x_range)
      y = random.uniform(0,self.y_range)
      new_tiger = Tiger([int(x),int(y)])
      self.tiger_d[new_tiger] = [x,y]
      exec('self.tiger_'+str(int(x)//12)+'_'+str(int(y)//12)+'[new_tiger]=[x,y]')
  
  # Generate corresponding grass in the world according to user input parameters.
  def generate_food(self, num_trees, num_forests, forest_epicenter = [-1,-1]):
    if len(forest_epicenter)>0 and forest_epicenter[0]==-1:
      forest_epicenter = [(np.random.uniform(0, self.x_range), np.random.uniform(0, self.y_range)) for i in range(num_forests)]
    if np.random.uniform(0,1)>0.9:
      print("New forest generated!!")
      num_forests = num_forests+1  
      forest_epicenter.append((np.random.uniform(0, self.x_range), np.random.uniform(0, self.y_range)))
    if np.random.uniform(0,1)>0.9:
      if num_forests>0:
        print("A forest is no longer able to sustain itself!!")
        num_forests = num_forests-1
        forest_epicenter.pop(np.random.randint(0,len(forest_epicenter)))
      if num_forests == 0:
        print("There will be scarcity of food. No one will survive!!")  
      
    forest_density = np.array([(np.random.randint(1,num_trees//num_forests)) for i in range(num_forests)])
    remaining = num_trees - np.sum(forest_density)
    forest_density = (remaining//num_forests)*np.ones(forest_density.shape)+forest_density
    
    for i in range(num_forests):
      for j in range(int(forest_density[i])):
        x = int((forest_epicenter[i][0]+np.random.normal(0,50))%self.x_range)
        y = int((forest_epicenter[i][1]+np.random.normal(0,50))%self.y_range)
        new_food = Food([x,y])
        exec('self.food_'+str(x//12)+'_'+str(y//12)+'[new_food] = [x,y]')
        self.food_d[new_food] = [x,y]

    return forest_epicenter
  
  # Update the behavior of all creatures in the world.(prey or move to prey)
  def eat_and_move(self):
      for Cow in self.cow_d.keys():
        pos=Cow.getPos()
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        self.dist = 999
        a = 'for food in self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  food_pos1 = self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[food] \n  if self.dist > math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2)\n    self.target_food = food\n    self.target_food_pos = food_pos1'
        exec(a)
        if self.dist < Cow.size+5+self.climate: 
            self.cow_d[Cow] = self.target_food_pos
            exec('self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Cow] = self.target_food_pos')
            Cow.move(self.target_food_pos)
            Cow.eat()
            exec('del self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_food]')
            del self.food_d[self.target_food]
        
        else:
            Cow.random_move((self.x_range,self.y_range))
            exec('del self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Cow]')
            pos=Cow.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Cow] = pos')
            self.cow_d[Cow] = pos
      for Sheep in self.sheep_d.keys():
        pos=Sheep.getPos()
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        self.dist = 999
        a = 'for food in self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  food_pos1 = self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[food] \n  if self.dist > math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2)\n    self.target_food = food\n    self.target_food_pos = food_pos1'
        exec(a)
        if self.dist < Sheep.size+5+self.climate: 
            self.sheep_d[Sheep] = self.target_food_pos
            exec('self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] = self.target_food_pos')
            Sheep.move(self.target_food_pos)
            Sheep.eat()
            exec('del self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_food]')
            del self.food_d[self.target_food]
            
        else:
            Sheep.random_move((self.x_range,self.y_range))
            exec('del self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep]')
            pos=Sheep.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] = pos')
            self.sheep_d[Sheep] = pos  

      for Tiger in self.tiger_d.keys():
        pos=Tiger.getPos()
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        self.dist = 999
       
        '''
        b = 'for Cow in self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_pos1 = self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Cow] \n  if self.dist > math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2)\n    self.target_prey = Cow\n    self.target_prey_pos = prey_pos1'
        exec(b)
        b = 'for Sheep in self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_s_pos1 = self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] \n  if self.dist > math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2)\n    self.target_prey = Sheep\n    self.target_prey_pos = prey_s_pos1'
        exec(b)
        '''
        if creatureXblock != 0 and creatureXblock != 50 and creatureYblock != 0 and creatureYblock != 50:
          b = 'for Sheep in self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_s_pos1 = self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] \n  if self.dist > math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2)\n    self.target_prey = Sheep\n    self.target_prey_pos = prey_s_pos1\nfor Sheep in self.sheep_'+str(creatureXblock-1)+'_'+str(creatureYblock)+': \n  prey_s_pos1 = self.sheep_'+str(creatureXblock-1)+'_'+str(creatureYblock)+'[Sheep] \n  if self.dist > math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2)\n    self.target_prey = Sheep\n    self.target_prey_pos = prey_s_pos1\nfor Sheep in self.sheep_'+str(creatureXblock+1)+'_'+str(creatureYblock)+': \n  prey_s_pos1 = self.sheep_'+str(creatureXblock+1)+'_'+str(creatureYblock)+'[Sheep] \n  if self.dist > math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2)\n    self.target_prey = Sheep\n    self.target_prey_pos = prey_s_pos1\nfor Sheep in self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock-1)+': \n  prey_s_pos1 = self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock-1)+'[Sheep] \n  if self.dist > math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2)\n    self.target_prey = Sheep\n    self.target_prey_pos = prey_s_pos1\nfor Sheep in self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock+1)+': \n  prey_s_pos1 = self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock+1)+'[Sheep] \n  if self.dist > math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2)\n    self.target_prey = Sheep\n    self.target_prey_pos = prey_s_pos1'
          exec(b)
          b = 'for Cow in self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_pos1 = self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Cow] \n  if self.dist > math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2)\n    self.target_prey = Cow\n    self.target_prey_pos = prey_pos1\nfor Cow in self.cow_'+str(creatureXblock-1)+'_'+str(creatureYblock)+': \n  prey_pos1 = self.cow_'+str(creatureXblock-1)+'_'+str(creatureYblock)+'[Cow] \n  if self.dist > math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2)\n    self.target_prey = Cow\n    self.target_prey_pos = prey_pos1\nfor Cow in self.cow_'+str(creatureXblock+1)+'_'+str(creatureYblock)+': \n  prey_pos1 = self.cow_'+str(creatureXblock+1)+'_'+str(creatureYblock)+'[Cow] \n  if self.dist > math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2)\n    self.target_prey = Cow\n    self.target_prey_pos = prey_pos1\nfor Cow in self.cow_'+str(creatureXblock)+'_'+str(creatureYblock-1)+': \n  prey_pos1 = self.cow_'+str(creatureXblock)+'_'+str(creatureYblock-1)+'[Cow] \n  if self.dist > math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2)\n    self.target_prey = Cow\n    self.target_prey_pos = prey_pos1\nfor Cow in self.cow_'+str(creatureXblock)+'_'+str(creatureYblock+1)+': \n  prey_pos1 = self.cow_'+str(creatureXblock)+'_'+str(creatureYblock+1)+'[Cow] \n  if self.dist > math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2)\n    self.target_prey = Cow\n    self.target_prey_pos = prey_pos1'
          exec(b)
        else:
          b = 'for Sheep in self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_s_pos1 = self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] \n  if self.dist > math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2)\n    self.target_prey = Sheep\n    self.target_prey_pos = prey_s_pos1'
          exec(b)
          b = 'for Cow in self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_pos1 = self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Cow] \n  if self.dist > math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2)\n    self.target_prey = Cow\n    self.target_prey_pos = prey_pos1'
          exec(b)
        if self.dist < Tiger.size+5+self.climate: 
            #if Tiger.health < 100 or Tiger.fertility < 40:
            #Tiger.health -= self.dist*0.02
            self.tiger_d[Tiger] = self.target_prey_pos
            c0 = self.target_prey_pos[0]//12
            c1 = self.target_prey_pos[1]//12
            exec('del self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Tiger]')
            exec('self.tiger_'+str(c0)+'_'+str(c1)+'[Tiger] = self.target_prey_pos')
            Tiger.move(self.target_prey_pos)
            Tiger.eat()
            if self.target_prey in self.cow_d:
              del self.cow_d[self.target_prey]
              exec('del self.cow_'+str(c0)+'_'+str(c1)+'[self.target_prey]')
            else:
              del self.sheep_d[self.target_prey]
              exec('del self.sheep_'+str(c0)+'_'+str(c1)+'[self.target_prey]')
            
        else:
            #Tiger.health -= (Tiger.size+5+self.climate)*0.02
            if self.dist != 999:
              pos_dif = [0,0]
              pos_dif[0] = self.target_prey_pos[0]-pos[0]
              pos_dif[1] = self.target_prey_pos[1]-pos[1]
              pos_dif_range =[0,0]
              pos_dif_range[0] = pos_dif[0]/math.sqrt(pos_dif[0]**2+pos_dif[1]**2)
              pos_dif_range[1] = pos_dif[1]/math.sqrt(pos_dif[0]**2+pos_dif[1]**2)
              x = int(pos[0]+(Tiger.size+5+self.climate)*pos_dif_range[0])
              y = int(pos[1]+(Tiger.size+5+self.climate)*pos_dif_range[1])
              if x<=600 and x>=0 and y<=600 and y>=0:
                self.tiger_d[Tiger] = [x,y]
                c0 = x//12
                c1 = y//12
                exec('del self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Tiger]')
                exec('self.tiger_'+str(c0)+'_'+str(c1)+'[Tiger] = [x,y]')
                Tiger.move([x,y])
              else:
                self.dist = 999

            if self.dist == 999:
              Tiger.random_move((self.x_range,self.y_range))
              exec('del self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Tiger]')
              pos=Tiger.getPos()
              creatureXblock=pos[0]//self.blocksize[0]
              creatureYblock=pos[1]//self.blocksize[1]
              exec('self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Tiger] = pos')
              self.tiger_d[Tiger] = pos

  # Determine the survival and reproduction of creature.
  def reset_creatures(self):
    for cow in list(self.cow_d.keys()):
          if cow.health <100 or cow.life <= 0:  
            pos=cow.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('del self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[cow]')
            del self.cow_d[cow] 
          elif cow.fertility > 0:
            cow.life = cow.life-1
            p = Cow(cow.getPos(),cow.speed+np.random.randint(-10,10))
            pos = p.getPos()
            self.cow_d[p] = pos
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[p] = pos')
            cow.newIteration()
          else:
            cow.life = cow.life-1
    
    for sheep in list(self.sheep_d.keys()):

          if sheep.health <100 or sheep.life <= 0:  
            pos=sheep.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('del self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[sheep]')
            del self.sheep_d[sheep]
          elif sheep.fertility > 0:
            sheep.life = sheep.life-1
            #for i in range(np.random.randint(0,3)):
            p = Sheep(sheep.getPos(),sheep.speed+np.random.randint(-10,10))
            pos = p.getPos()
            self.sheep_d[p] = pos
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[p] = pos')
            sheep.newIteration()
          else:
            sheep.life = sheep.life-1
    
    for tiger in list(self.tiger_d.keys()):
          if tiger.health <120 or tiger.life <= 0:   
            pos=tiger.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]

            exec('del self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[tiger]')
            del self.tiger_d[tiger]

          elif tiger.fertility > 40:
            tiger.life = tiger.life-2
            p = Tiger(tiger.getPos(),tiger.speed+np.random.randint(-10,10))
            pos = p.getPos()

            self.tiger_d[p] = pos
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]

            exec('self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[p] = pos')
            tiger.newIteration()
          else:
            tiger.life = tiger.life-1


  def clear_food(self):
      for food in self.food_d:
          pos = food.getPos()
          creatureXblock=pos[0]//self.blocksize[0]
          creatureYblock=pos[1]//self.blocksize[1]
          exec('del self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[food]')
      self.food_d = {}

##GUI
  def print_food(self,gameDisplay):
        '''
        Print function for the food present; draws a rectangle(representing food) in the gameDisplay.
        '''
        for food in self.food_d:
          draw.circle(gameDisplay,food.color,food.getPos(),food.size)

  def print_creatures(self,gameDisplay):
        '''
        Print function for the creatures present; draws a circle corresponding to the creature's position in gameDisplay.
        '''
        for Cow in self.cow_d:
            draw.circle(gameDisplay,Cow.color,Cow.getPos(),4)
        for Sheep in self.sheep_d:
            draw.circle(gameDisplay,Sheep.color,Sheep.getPos(),4)
        for Tiger in self.tiger_d:
            draw.circle(gameDisplay,Tiger.color,Tiger.getPos(),6)

    ##
  

  # The purpose is the same as eat_and_move, but more advanced in predation strategy.
  def sensitive_eat_and_move(self,prey_net,predator_net):
    p1 = torch.tensor([0,0]).cuda(device=torch.device(0))
    p2 = torch.tensor([0,0]).cuda(device=torch.device(0))
    prey_xy_prey = torch.ones(len(self.cow_d),len(self.tiger_d),2).cuda(device=torch.device(0))
    prey_xy_predator = torch.ones(len(self.tiger_d),len(self.tiger_d),2).cuda(device=torch.device(0))
    predator_xy_prey = torch.ones(len(self.cow_d),len(self.cow_d),2).cuda(device=torch.device(0))
    predator_xy_predator = torch.ones(len(self.tiger_d),len(self.cow_d),2).cuda(device=torch.device(0))
    D_prey = torch.ones(len(self.cow_d),len(self.tiger_d)).cuda(device=torch.device(0))
    D_predator = torch.ones(len(self.tiger_d),len(self.cow_d)).cuda(device=torch.device(0))
    L_prey = torch.zeros(len(self.cow_d)).long().cuda(device=torch.device(0))
    L_predator = torch.zeros(len(self.tiger_d)).long().cuda(device=torch.device(0))


    for i, prey in enumerate(self.cow_d.keys()):
      pos = prey.getPos()
      prey_xy_prey[i,:,0] = pos[0]
      prey_xy_prey[i,:,1] = pos[1]
      predator_xy_prey[i,:,0] = pos[0]
      predator_xy_prey[i,:,1] = pos[1]

    for j, predator in enumerate(self.tiger_d.keys()):
      pos = predator.getPos()
      prey_xy_predator[j,:,0] = pos[0]
      prey_xy_predator[j,:,1] = pos[1]
      predator_xy_predator[j,:,0] = pos[0]
      predator_xy_predator[j,:,1] = pos[1]

    for i in range(prey_xy_prey.size(dim=0)):
      for j in range(prey_xy_predator.size(dim=0)):
        m = torch.square(prey_xy_prey[i,j,0] - prey_xy_predator[j,j,0])
        n = torch.square(prey_xy_prey[i,j,1] - prey_xy_predator[j,j,1])
        d = torch.sqrt(m+n)
        D_prey[i][j] = d
    
    D_prey = torch.sort(D_prey,dim=1,descending=False)

    for j in range(predator_xy_predator.size(dim=0)):
      for i in range(predator_xy_prey.size(dim=0)):
        m = torch.square(predator_xy_predator[j,i,0] - predator_xy_prey[i,i,0])
        n = torch.square(predator_xy_predator[j,i,1] - predator_xy_prey[i,i,1])
        d = torch.sqrt(m+n)
        D_predator[j,i] = d
    
    D_predator = torch.sort(D_predator,dim=1,descending=False)
    
    if len(D_prey[0]) >=1 and len(D_predator[0]) >=2:
      Input_prey = D_prey[0][:,:2]
      Input_prey = Input_prey - torch.mean(Input_prey,dim=1).reshape((len(Input_prey),1))
      # Input_prey.cuda(device=torch.device(0))
      # Input_prey = torch.divide(Input_prey,torch.std(Input_prey,dim=1).reshape((len(Input_prey),1)))
      
      # prey_net = Prey_nn(2,8,2)
      prey_optim = torch.optim.SGD(prey_net.parameters(), lr=0.01)
      prey_loss_func = torch.nn.CrossEntropyLoss()
      prey_out = prey_net(Input_prey)
      prey_loss = prey_loss_func(prey_out,L_prey)
      prey_optim.zero_grad()
      prey_loss.backward()
      prey_optim.step()
    
    if len(D_predator[0]) >=1 and len(D_prey[0]) >=2:
      Input_predator = D_predator[0][:,:2]
      Input_predator = Input_predator - torch.mean(Input_predator,dim=1).reshape((len(Input_predator),1))
      Input_predator.cuda(device=torch.device(0))
      # Input_predator = torch.divide(Input_predator,torch.std(Input_predator,dim=1).reshape((len(Input_predator),1)))

      # predator_net = Predator_nn(2,8,2)
      predator_optim = torch.optim.SGD(predator_net.parameters(), lr=0.005)
      predator_loss_func = torch.nn.CrossEntropyLoss()
      predator_out = predator_net(Input_predator)
      predator_loss = predator_loss_func(predator_out,L_predator)
      predator_optim.zero_grad()
      predator_loss.backward()

      predator_optim.step()

    if len(D_prey[0]) >=1 and len(D_predator[0]) >=2:
      for i, prey in enumerate(self.cow_d.keys()):
      # if predator.moveflag:
        pos=prey.getPos()
        
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        # if creatureXblock >= 51:
        #       creatureXblock = 50
        # if creatureYblock >= 51:
        #       creatureYblock = 50
        self.dist = 999
        j =  D_prey[1][i][0].cpu()
        
        d = D_prey[0][i][0].cpu()
        if (d.numpy() != 0):
          direct = torch.divide((prey_xy_prey[i,j] - prey_xy_predator[j,j]),d)
          direct = direct.cpu().numpy()
        else:
          direct = np.array([0,0])
        a = 'for food in self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  food_pos1 = self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[food] \n  if self.dist > math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2)\n    self.target_food = food\n    self.target_food_pos = food_pos1'        
        exec(a)
        if self.dist < prey.size+5: 
            self.cow_d[prey] = self.target_food_pos
            exec('self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey] = self.target_food_pos')
            prey.move(self.target_food_pos)
            prey.eat()
            exec('del self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_food]')
            del self.food_d[self.target_food]
        
        else:
          if len(D_prey[0][i])>= 2:
              p1 = prey_out[i] 

              p1 = p1.cpu().detach().numpy()
              value = np.random.choice([0,1],p=p1)   
              if value == 0:
                prey.sensitive_move((self.x_range,self.y_range),direct)
                
                t = prey.getPos()

              else:
                prey.random_move((self.x_range,self.y_range))

          elif len(D_prey[0][i,:].size()) == 1:
            p1 = np.array([1,1])
            p1 = p1.cpu().detach().numpy()
            prey.random_move((self.x_range,self.y_range))

          else:
            p1 = np.array([0,0])
            p1 = p1.cpu().detach().numpy()
            
          exec('del self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey]')
          pos=prey.getPos()
          creatureXblock=pos[0]//self.blocksize[0]
          creatureYblock=pos[1]//self.blocksize[1]
          exec('self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey] = pos')
          self.cow_d[prey] = pos
    else:
      for i, prey in enumerate(self.cow_d.keys()):
        
        pos=prey.getPos()
        
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        prey.random_move((self.x_range,self.y_range))
        exec('del self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey]')
        pos=prey.getPos()
        
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        
        
        exec('self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey] = pos')
        if len(self.cow_d != 1):self.cow_d[prey] = pos
      
    if len(D_predator[0]) >=1 and len(D_prey[0]) >=2:
      for i, predator in enumerate(self.tiger_d.keys()):
        pos=predator.getPos()
        
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        self.dist = 999

        j =  D_predator[1][i][0].cpu()
        
        d = D_predator[0][i][0].cpu()
        if (d.numpy() != 0):
          direct = torch.divide((-predator_xy_predator[i,j] + predator_xy_prey[j,j]),d)
          direct = direct.cpu().numpy()
        else:
          direct = np.array([0,0])
        a = 'for prey in self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_pos1 = self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey] \n  if self.dist > math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2)\n    self.target_prey = prey\n    self.target_prey_pos = prey_pos1'
        b = 'for Sheep in self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_s_pos1 = self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] \n  if self.dist > math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2)\n    self.target_prey = Sheep\n    self.target_prey_pos = prey_s_pos1'
        
        exec(a)
        exec(b)
        if self.dist < predator.size+5: 
            self.tiger_d[predator] = self.target_prey_pos
            exec('self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[predator] = self.target_prey_pos')
            predator.move(self.target_prey_pos)
            predator.eat()
            if self.target_prey in self.cow_d:
                del self.cow_d[self.target_prey]
                exec('del self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_prey]')
            else:
                del self.sheep_d[self.target_prey]
                exec('del self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_prey]')
        else:
            if len(D_predator[0][i])>= 2:
              p2 = predator_out[i]     
              p2 = p2.cpu().detach().numpy()
              value = np.random.choice([0,1],p=p2)   
              if value == 0:
                predator.sensitive_move((self.x_range,self.y_range),direct)

              else:
                predator.random_move((self.x_range,self.y_range))

            elif len(D_predator[0][i,:].size()) == 1:
              p2 = np.array([1,1])
              predator.random_move((self.x_range,self.y_range))    

            else:
              p2 = np.array([0,0])

            exec('del self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[predator]')
            pos=predator.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[predator] = pos')
            self.tiger_d[predator] = pos
    else: 
      for i, predator in enumerate(self.tiger_d.keys()):
        pos=predator.getPos()
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        predator.random_move((self.x_range,self.y_range))
        exec('del self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[predator]')
        pos=predator.getPos()
        
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        
        
        exec('self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[predator] = pos')
        self.tiger_d[predator] = pos
    
    
    for Sheep in self.sheep_d.keys():
        pos=Sheep.getPos()
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        self.dist = 999
        a = 'for food in self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  food_pos1 = self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[food] \n  if self.dist > math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2)\n    self.target_food = food\n    self.target_food_pos = food_pos1'
        exec(a)
        if self.dist < Sheep.size+5: 
           
            self.sheep_d[Sheep] = self.target_food_pos
            exec('self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] = self.target_food_pos')
            Sheep.move(self.target_food_pos)
            Sheep.eat()
            exec('del self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_food]')
            del self.food_d[self.target_food]
        
        else:
            Sheep.random_move((self.x_range,self.y_range))
            exec('del self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep]')
            pos=Sheep.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] = pos')
            self.sheep_d[Sheep] = pos
        
    return p1, p2
    
      
