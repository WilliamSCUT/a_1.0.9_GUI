import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import numpy.linalg as LA
import math

class Creature():
    def __init__(self,starting_pos=[0,0],speed=np.random.randint(10,20),size=np.random.randint(1,10),life = np.random.randint(1,5)):
        '''
        def colorfunc(speed):
            if speed<10:
                return (10,255,0)
            elif speed<=50:
                return (speed*5,2550/speed,0)
            else:
                return (255,0,0)
        '''
        self.starting_pos=np.array(starting_pos)
        self.health = 100
        self.fertility=0                 #生育能力
        self.pos=np.array(starting_pos)
        self.moveflag=True
        self.content=False
        self.theta = 2 * np.pi * np.random.rand() - np.pi
        self.size = size 
                        #生物大小
        if speed<0:
            self.speed = 2
        else:
            self.speed=speed
        '''
        self.speed_color = colorfunc(self.speed) #用不同的颜色来代表不同的速度
        '''

        #self.size = 5              #这里似乎限定了大小
        #接下来是自己加的，这个life属性我还没用上，后面可以在迭代里面加上对life的限制
        self.life = life


    def getPos(self):
        return [int(self.pos[0]),int(self.pos[1])]

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
            self.theta = self.theta - np.pi/2 
            
        if self.pos[0]>=worldSz[0]:
            self.pos[1]=pos_0
            self.theta = np.pi - self.theta

        if self.pos[1]<0:
            self.pos[1]=worldSz[1]+pos_1
            #self.pos[1]=0
            self.theta = self.theta - np.pi/2


        if self.pos[1]>=worldSz[1]:
            self.pos[1]=pos_1
            #self.pos[1]=worldSz[1]-1
            self.theta = -self.theta

        self.pos = np.array([int(self.pos[0]),int(self.pos[1])])


    def move(self,pos): 
        # if(self.moveflag==True):

        #这个move的参数已经改了，传入的参数pos是目标猎物的坐标


            # decrease in health with every step
            #这里如果健康小于0似乎不能动，而每次移动都是随机的，应该要改

            #这些可能要考虑怎么写合理一点，我没怎么改
            self.health = self.health -self.speed/50
            if self.health<=0:
                self.moveflag=False
            '''
            self.theta = self.theta + 0.5*(np.random.rand()) - 0.25
            velocity = self.speed * np.array([np.cos(self.theta),np.sin(self.theta)])
            self.pos = self.pos + velocity * 0.13                    
            

            # self.pos[0]=np.random.randint(-1,2)+self.pos[0]
            # self.pos[1]=np.random.randint(-1,2)+self.pos[1]
            #这里是边界限制条件，到后期可能要分析theta的作用
            if self.pos[0]<0:
                self.pos[0]=0
                self.theta = self.theta - np.pi/2 
            
            if self.pos[0]>=worldSz[0]:
                self.pos[0]=worldSz[0]-1
                self.theta = np.pi - self.theta

            if self.pos[1]<0:
                self.pos[1]=0
                self.theta = self.theta - np.pi/2


            if self.pos[1]>=worldSz[1]:
                self.pos[1]=worldSz[1]-1
                self.theta = -self.theta

            '''
            #直接把捕食者的坐标改到猎物身上
            self.pos = np.array([int(pos[0]),int(pos[1])]) 
    '''
    def eat(self):
        # print("EATEN")
        if (self.fertility<100):
            if (self.content==False):
                 self.content=True        
            else:
                self.moveflag=False
                self.fertility=100         #拉满生育值
    '''
    def eat(self):                  
        if (self.fertility<100):
      
            if self.health<70 or self.fertility<70:
                self.health+=30
                self.fertility+=50
        #self.content=True
      
        else:
            self.moveflag=False

    def newIteration(self):
        '''
        if (self.content==True):
            self.health=100
            self.content=False
            '''
        self.fertility=0
        self.moveflag=True
        # self.pos=self.starting_pos
