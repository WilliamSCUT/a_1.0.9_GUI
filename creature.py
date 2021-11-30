'''
creature.py
1.Define the basic class which is called Creature.
2.This class is the parent class of each creature class(Cow,Sheep...)
3.Define five functions related to the action of the creature.
'''
import numpy as np
import random
import numpy.linalg as LA
import math

class Creature():
    # Initialize the creature when creating it with position,speed,size,life.
    def __init__(self,starting_pos=[0,0],speed=np.random.randint(10,20),size=np.random.randint(1,10),life = np.random.randint(1,5)):
        self.starting_pos=np.array(starting_pos)
        self.health = 100
        self.fertility=0                 
        self.pos=np.array(starting_pos)
        self.moveflag=True
        self.theta = 2 * np.pi * np.random.rand() - np.pi
        self.size = size 
        if speed<0:
            self.speed = 2
        else:
            self.speed=speed
        self.life = life

    # Get the position of the creature.
    def getPos(self):
        return [int(self.pos[0]),int(self.pos[1])]

    # Hunting around for food.
    def random_move(self,worldSz):
        self.health = self.health -self.speed/50
        if self.health<=0:
            self.moveflag=False
        self.theta = self.theta + 0.5*(np.random.rand()) - 0.25
        velocity = self.speed * np.array([np.cos(self.theta),np.sin(self.theta)])
        self.pos = self.pos + velocity * 0.13      
        pos_0=self.pos[0]//worldSz[0]
        pos_1=self.pos[1]//worldSz[1]    
        if self.pos[0]<0:
            self.pos[0]=worldSz[0]+pos_0
            #self.theta = self.theta - np.pi/2 
            
        if self.pos[0]>=worldSz[0]:
            self.pos[0]=pos_0
            #self.theta = np.pi - self.theta

        if self.pos[1]<0:
            self.pos[1]=worldSz[1]+pos_1
            #self.pos[1]=0
            #self.theta = self.theta - np.pi/2


        if self.pos[1]>=worldSz[1]:
            self.pos[1]=pos_1
            #self.pos[1]=worldSz[1]-1
            #self.theta = -self.theta

        self.pos = np.array([int(self.pos[0]),int(self.pos[1])])

    # Advanced option. Track the nearest food.
    def sensitive_move(self,worldSz,direct):
        self.health = self.health -self.speed/50
        if self.health<=0:
            self.moveflag=False
        
        velocity = self.speed * np.array([direct[0],direct[1]])
        self.pos = self.pos + velocity * 0.13      
        pos_0=self.pos[0]//worldSz[0]
        pos_1=self.pos[1]//worldSz[1]  
        #print(pos_0,pos_1)
        
        if self.pos[0]<0:
            self.pos[0]=worldSz[0]+pos_0
            # if self.pos[0] > 600:
            #     print(1)
            #self.theta = self.theta - np.pi/2 
            
        if self.pos[0]>=worldSz[0]:
            self.pos[0]=pos_0
            # if self.pos[0] > 600:
            #     print(1)
            #self.theta = np.pi - self.theta

        if self.pos[1]<0:
            self.pos[1]=worldSz[1]+pos_1
            #self.pos[1]=0
            #self.theta = self.theta - np.pi/2


        if self.pos[1]>=worldSz[1]:
            self.pos[1]=pos_1
            #self.pos[1]=worldSz[1]-1
            #self.theta = -self.theta
        
        self.pos = np.array([int(self.pos[0]),int(self.pos[1])])

    # After moving, change its own pos.
    def move(self,pos): 
            self.health = self.health -self.speed/50
            self.pos = np.array([int(pos[0]),int(pos[1])]) 

    # Renew the fertility after giving birth.
    def newIteration(self):
        self.fertility=0
        self.moveflag=True

