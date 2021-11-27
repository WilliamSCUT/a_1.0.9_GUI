import pygame
from pygame import *
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import numpy.linalg as LA
import math
from creature import Creature
from predator import Predator
from prey import Prey
from prey_s import Prey_s
from food import Food

class World():
  def __init__(self):
    self.x_range = 600
    self.y_range = 600

    #self.food_pos1 = 0
    # self.food = np.array([])
    #这些是原程序结构，下面这些目前还会用到
    self.numBlocksx=50
    self.numBlocksy=50
    self.blocksize=np.array([self.x_range//self.numBlocksx,self.y_range//self.numBlocksy])
    
    self.predators_d = {}
    self.prey_d = {}
    self.dist = 999
    self.target_food = Food([0,0])
    self.target_food_pos = []
    self.target_prey = Prey([0,0])
    self.target_prey_pos = []
    #1.0.9
    self.prey_s_d = {}
    self.target_prey_s = Prey_s([0,0])
    self.target_prey_s_pos = []
    #1.0.3版本更新
    #方便GUI画图
    self.food_d = {}
    

    start=0

    #这是我们的三种字典创建，后面可以考虑搞个东西把那么多个字典存起来
    for i in range(51):
        for j in range(51):
            name = 'self.prey_'+str(i)+'_'+str(j)
            exec(name+'={}')
            name = 'self.prey_s_'+str(i)+'_'+str(j)
            exec(name+'={}')
            name_p= 'self.predator_'+str(i)+'_'+str(j)
            exec(name_p+'={}')
            name_f= 'self.food_'+str(i)+'_'+str(j)
            exec(name_f+'={}')



  def initialize_creatures(self, number_of_prey,number_of_prey_s,number_of_predator):
    for i in range(0, number_of_prey):
      new_prey = Prey([random.uniform(0,self.x_range),random.uniform(0,self.y_range)])    
      pos = new_prey.getPos()
      #这是目前我们的存储容器，字典
      #1.0.2更新，这里直接变成更新字典，应改为追加
      #exec('self.prey_'+str(pos[0]//self.blocksize[0])+'_'+str(pos[1]//self.blocksize[1])+'={new_prey:pos}')
      exec('self.prey_'+str(pos[0]//self.blocksize[0])+'_'+str(pos[1]//self.blocksize[1])+'[new_prey]=pos')
      #1.0.2更新 这里也是用一个字典来存整个prey,优点在于删除的时间复杂度为1
      self.prey_d[new_prey] = pos
      # self.prey=np.hstack((self.prey,Prey([150,300])))

    for i in range(0, number_of_prey_s):
      new_prey_s = Prey_s([random.uniform(0,self.x_range),random.uniform(0,self.y_range)])    
      pos = new_prey_s.getPos()
      #这是目前我们的存储容器，字典
      #1.0.2更新，这里直接变成更新字典，应改为追加
      #exec('self.prey_'+str(pos[0]//self.blocksize[0])+'_'+str(pos[1]//self.blocksize[1])+'={new_prey:pos}')
      exec('self.prey_s_'+str(pos[0]//self.blocksize[0])+'_'+str(pos[1]//self.blocksize[1])+'[new_prey_s]=pos')
      #1.0.2更新 这里也是用一个字典来存整个prey,优点在于删除的时间复杂度为1
      self.prey_s_d[new_prey_s] = pos


    for i in range(0, number_of_predator):
      x = random.uniform(0,self.x_range)
      y = random.uniform(0,self.y_range)
      new_predator = Predator([int(x),int(y)])
      
      #这是目前我们的存储容器，字典
      #1.0.2更新，这里直接变成更新字典，应改为追加
      #exec('self.predator_'+str(int(x)//50)+'_'+str(int(y)//50)+'={new_predator:[x,y]}')
      self.predators_d[new_predator] = [x,y]
      exec('self.predator_'+str(int(x)//12)+'_'+str(int(y)//12)+'[new_predator]=[x,y]')
  
  def generate_food(self, num_trees, num_forests, forest_epicenter = [-1,-1]):
    if len(forest_epicenter)>0 and forest_epicenter[0]==-1:
      forest_epicenter = [(np.random.uniform(0, self.x_range), np.random.uniform(0, self.y_range)) for i in range(num_forests)]
    if np.random.uniform(0,1)>0.9:
      print("New forest generated!!")
      num_forests = num_forests+1  
      forest_epicenter.append((np.random.uniform(0, self.x_range), np.random.uniform(0, self.y_range)))
    #这里我感觉初始的森林太少了，影响体现在于：原程序中一般prey要移动很多次（一天的步长有300）之后才能吃到草，森林数量变多之后可能食物的分布会均匀一点？
    #因此在我定义的eat_and_move 函数里面求猎物和食物的距离的时候要迭代很多次才会遇见有食物的情况（一般直接发现每食物然后就pass）
    if np.random.uniform(0,1)>0.9:
      if num_forests>0:
        print("A forest is no longer able to sustain itself!!")
        print(len(forest_epicenter))
        num_forests = num_forests-1
        forest_epicenter.pop(np.random.randint(0,len(forest_epicenter)))
        print(len(forest_epicenter))
      if num_forests == 0:
        print("There will be scarcity of food. No one will survive!!")  
      
    
    forest_density = np.array([(np.random.randint(1,num_trees//num_forests)) for i in range(num_forests)])
    remaining = num_trees - np.sum(forest_density)
    forest_density = (remaining//num_forests)*np.ones(forest_density.shape)+forest_density
    
    for i in range(num_forests):
      for j in range(int(forest_density[i])):
        x = int((forest_epicenter[i][0]+np.random.normal(0,50))%self.x_range)
        y = int((forest_epicenter[i][1]+np.random.normal(0,50))%self.y_range)
        foodnew=[x,y]
        
        #这是目前我们的存储容器，字典
        new_food = Food([x,y])
        #坐标测试
        '''
        x1 = str(x//12) 
        x2 = str(y//12)     
        x3 = int(foodnew[0])//self.blocksize[0]
        x4 = int(foodnew[1])//self.blocksize[1]
        '''
        #exec('self.food_'+str(x//12)+'_'+str(y//12)+'={new_food:[x,y]}')
        exec('self.food_'+str(x//12)+'_'+str(y//12)+'[new_food] = [x,y]')
        #1.0.3更新
        self.food_d[new_food] = [x,y]
        
    return forest_epicenter
  
  def eat_and_move(self):
      #1.0.2更新 变量更新
      for prey in self.prey_d.keys():
      # if predator.moveflag:
        pos=prey.getPos()
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        self.dist = 999
        #这是要执行的代码
        a = 'for food in self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  food_pos1 = self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[food] \n  if self.dist > math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2)\n    self.target_food = food\n    self.target_food_pos = food_pos1'
        #可以用print检验有无错误
        #print(a)
        exec(a)
        #print(dist)
        #exec('dist=dist+2')
        #print(dist)
        #下面这个判断条件是我随机加的，不一定好用，你们可以尝试通过计算得到一个相对合理的条件
        #1.0.2更新 变量更新
        if self.dist < prey.size+5: 
            #这个应该是牛（prey）移动到食物坐标，这里的move是原来的随机移动函数，我稍微改了一下，可能还有bug
            #这里应该还要调用eat函数，来更新牛吃到草后的属性更新
            #1.0.2更新，全局变量问题
            self.prey_d[prey] = self.target_food_pos
            exec('self.prey_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey] = self.target_food_pos')
            prey.move(self.target_food_pos)
            prey.eat()
            #这是上一种思路，想通过食物的坐标反推其字典里面的key值，不过zip生成的是一次性的迭代器所以好像比较难操作，目前换了一种思路
            '''
            exec('temp = zip(self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'.values(), self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'.keys())')
            temp1 = temp[food_get_pos]
            '''
            #这一步是删除被吃的猎物（草）
            exec('del self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_food]')
        #1.0.3更新 随机移动
            del self.food_d[self.target_food]
        
        else:
            prey.random_move((self.x_range,self.y_range))
            exec('del self.prey_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey]')
            pos=prey.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.prey_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey] = pos')
            self.prey_d[prey] = pos
      for prey_s in self.prey_s_d.keys():
      # if predator.moveflag:
        pos=prey_s.getPos()
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        self.dist = 999
        #这是要执行的代码
        a = 'for food in self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  food_pos1 = self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[food] \n  if self.dist > math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((food_pos1[0]-pos[0])**2+(food_pos1[1]-pos[1])**2)\n    self.target_food = food\n    self.target_food_pos = food_pos1'
        #可以用print检验有无错误
        #print(a)
        exec(a)
        #print(dist)
        #exec('dist=dist+2')
        #print(dist)
        #下面这个判断条件是我随机加的，不一定好用，你们可以尝试通过计算得到一个相对合理的条件
        #1.0.2更新 变量更新
        if self.dist < prey_s.size+5: 
            #这个应该是牛（prey）移动到食物坐标，这里的move是原来的随机移动函数，我稍微改了一下，可能还有bug
            #这里应该还要调用eat函数，来更新牛吃到草后的属性更新
            #1.0.2更新，全局变量问题
            self.prey_s_d[prey_s] = self.target_food_pos
            exec('self.prey_s_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey_s] = self.target_food_pos')
            prey_s.move(self.target_food_pos)
            prey_s.eat()
            #这是上一种思路，想通过食物的坐标反推其字典里面的key值，不过zip生成的是一次性的迭代器所以好像比较难操作，目前换了一种思路
            '''
            exec('temp = zip(self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'.values(), self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'.keys())')
            temp1 = temp[food_get_pos]
            '''
            #这一步是删除被吃的猎物（草）
            exec('del self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_food]')
        #1.0.3更新 随机移动
            del self.food_d[self.target_food]
        
        else:
            prey_s.random_move((self.x_range,self.y_range))
            exec('del self.prey_s_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey_s]')
            pos=prey_s.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.prey_s_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey_s] = pos')
            self.prey_s_d[prey_s] = pos  
            
                
      #1.0.2更新，已经改了
      #这下面还没改，等上面牛吃草完善好了之后应该可以直接相同思路copy
      #1.0.2更新，for循环也改了，你们可以和原版比较一下
      for predator in self.predators_d.keys():
      # if predator.moveflag:
        pos=predator.getPos()
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        #1.0.2更新 变量更新
        self.dist = 999
        b = 'for prey in self.prey_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_pos1 = self.prey_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey] \n  print(prey_pos1)\n  if self.dist > math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2)\n    self.target_prey = prey\n    self.target_prey_pos = prey_pos1'
      # if predator.moveflag:
        exec(b)
        b = 'for prey_s in self.prey_s_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_s_pos1 = self.prey_s_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey_s] \n  print(prey_s_pos1)\n  if self.dist > math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2)\n    self.target_prey = prey_s\n    self.target_prey_pos = prey_s_pos1'
        exec(b)
        #1.0.2更新 变量更新
        if self.dist < predator.size+5: 
            #这个应该是牛（prey）移动到食物坐标，这里的move是原来的随机移动函数，我稍微改了一下，可能还有bug
            #1.0.2更新 变量更新
            self.predators_d[predator] = self.target_prey_pos
            exec('self.predator_'+str(creatureXblock)+'_'+str(creatureYblock)+'[predator] = self.target_prey_pos')
            predator.move(self.target_prey_pos)
            predator.eat()
            #这是上一种思路，想通过食物的坐标反推其字典里面的key值，不过zip生成的是一次性的迭代器所以好像比较难操作，目前换了一种思路
            '''
            exec('temp = zip(self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'.values(), self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'.keys())')
            temp1 = temp[food_get_pos]
            '''
            #这一步是删除被吃的猎物（草）
            #1.0.2更新 除了删除对应50*50字典里的prey，还删除了存所有prey的字典：prey_d里面的prey
            if self.target_prey in self.prey_d:
              del self.prey_d[self.target_prey]
              exec('del self.prey_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_prey]')
            else:
              del self.prey_s_d[self.target_prey]
              exec('del self.prey_s_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_prey]')

        #1.0.3更新 随机移动
        else:
            predator.random_move((self.x_range,self.y_range))
            exec('del self.predator_'+str(creatureXblock)+'_'+str(creatureYblock)+'[predator]')
            pos=predator.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.predator_'+str(creatureXblock)+'_'+str(creatureYblock)+'[predator] = pos')
            self.predators_d[predator] = pos
        '''
        else:
            predator.random_move((self.x_range,self.y_range))
            '''
  #1.0.3更新 死亡迭代，繁殖迭代
  def reset_creatures(self):
    for prey in list(self.prey_d.keys()):
          #死亡
          if prey.health <100 or prey.life <= 0:   #似乎等价于creature.content不为false
            pos=prey.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            #从两个字典里面都要删除
            exec('del self.prey_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey]')
            del self.prey_d[prey]
          #繁殖  
          elif prey.fertility > 0:
            prey.life = prey.life-1
            p = Prey(prey.getPos(),prey.speed+np.random.randint(-10,10))
            pos = p.getPos()
            # print("New prey added")
            self.prey_d[p] = pos
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.prey_'+str(creatureXblock)+'_'+str(creatureYblock)+'[p] = pos')
            prey.newIteration()
    
    for prey_s in list(self.prey_s_d.keys()):
          #死亡
          if prey_s.health <100 or prey_s.life <= 0:   #似乎等价于creature.content不为false
            pos=prey_s.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            #从两个字典里面都要删除
            exec('del self.prey_s_'+str(creatureXblock)+'_'+str(creatureYblock)+'[prey_s]')
            del self.prey_s_d[prey_s]
          #繁殖  
          elif prey_s.fertility > 0:
            prey_s.life = prey_s.life-1
            p = Prey_s(prey_s.getPos(),prey_s.speed+np.random.randint(-10,10))
            pos = p.getPos()
            # print("New prey added")
            self.prey_s_d[p] = pos
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.prey_s_'+str(creatureXblock)+'_'+str(creatureYblock)+'[p] = pos')
            prey_s.newIteration()
    
    # self.prey = np.array(new_prey)
        
    for predator in list(self.predators_d.keys()):
          #死亡
          print(predator.health)
          if predator.health <100 or predator.life <= 0:   #似乎等价于creature.content不为false
            pos=predator.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            #从两个字典里面都要删除
            exec('del self.predator_'+str(creatureXblock)+'_'+str(creatureYblock)+'[predator]')
            del self.predators_d[predator]
          #繁殖
          elif predator.fertility > 0:
            predator.life = predator.life-1
            p = Prey(predator.getPos(),predator.speed+np.random.randint(-10,10))
            pos = p.getPos()
            # print("New prey added")
            self.predators_d[p] = pos
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.predator_'+str(creatureXblock)+'_'+str(creatureYblock)+'[p] = pos')
            predator.newIteration()

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
        # for x in range(50):
        #     for y in range(50):
        #         name = {}
        #         name_f= 'self.food_'+str(x)+'_'+str(y)
        #         exec('name' + '=' +name_f)
        #         if list(name) != {}:
        #             food = list(name)[0]
        #             pos = list(name.values())[0]
        #             draw.rect(gameDisplay,food[0].color,Rect(pos[0],pos[1],food[0].size,food[0].size))
        for food in self.food_d:
          draw.circle(gameDisplay,food.color,food.getPos(),food.size)
                # a = 'if list(self.food_'+str(x)+'_'+str(y)+') != []: \n  food = self.food_'+str(x)+'_'+str(y) +'\n  pos = self.food[0] \n  draw.rect(gameDisplay,list(self.food_'+str(x)+'_'+str(y)+')[0].color,Rect(pos[0],pos[1],list(self.food_'+str(x)+'_'+str(y)+')[0].size,list(self.food_'+str(x)+'_'+str(y)+')[0].size))'
                # exec(a)

  def print_creatures(self,gameDisplay):
        '''
        Print function for the creatures present; draws a circle corresponding to the creature's position in gameDisplay.
        '''
        for prey in self.prey_d:
            draw.circle(gameDisplay,prey.color,prey.getPos(),prey.size+2)
        for prey_s in self.prey_s_d:
            draw.circle(gameDisplay,prey_s.color,prey_s.getPos(),prey_s.size+2)
        for predator in self.predators_d:
            draw.circle(gameDisplay,predator.color,predator.getPos(),predator.size-1)


    ##