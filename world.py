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
from Tiger import Tiger
from Cow import Cow
from Sheep import Sheep
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
    
    self.tiger_d = {}
    self.cow_d = {}
    self.dist = 999
    self.target_food = Food([0,0])
    self.target_food_pos = []

    #1.0.9
    self.sheep_d = {}
    '''
    self.target_sheep = Sheep([0,0])
    self.target_sheep_pos = []
    self.target_cow = Cow([0,0])
    self.target_cow_pos = []
    '''
    self.target_prey = Cow([0,0])
    self.target_prey_pos = []
    #1.0.3版本更新
    #1.0.3版本更新
    #方便GUI画图
    self.food_d = {}
    

    start=0

    #这是我们的三种字典创建，后面可以考虑搞个东西把那么多个字典存起来
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



  def initialize_creatures(self, number_of_cow,number_of_sheep,number_of_tiger):
    for i in range(0, number_of_cow):
      new_cow = Cow([random.uniform(0,self.x_range),random.uniform(0,self.y_range)])    
      pos = new_cow.getPos()
      #这是目前我们的存储容器，字典
      #1.0.2更新，这里直接变成更新字典，应改为追加
      #exec('self.prey_'+str(pos[0]//self.blocksize[0])+'_'+str(pos[1]//self.blocksize[1])+'={new_prey:pos}')
      exec('self.cow_'+str(pos[0]//self.blocksize[0])+'_'+str(pos[1]//self.blocksize[1])+'[new_cow]=pos')
      #1.0.2更新 这里也是用一个字典来存整个prey,优点在于删除的时间复杂度为1
      self.cow_d[new_cow] = pos
      # self.Cow=np.hstack((self.Cow,Cow([150,300])))

    for i in range(0, number_of_sheep):
      new_sheep = Sheep([random.uniform(0,self.x_range),random.uniform(0,self.y_range)])    
      pos = new_sheep.getPos()
      #这是目前我们的存储容器，字典
      #1.0.2更新，这里直接变成更新字典，应改为追加
      #exec('self.prey_'+str(pos[0]//self.blocksize[0])+'_'+str(pos[1]//self.blocksize[1])+'={new_prey:pos}')
      exec('self.sheep_'+str(pos[0]//self.blocksize[0])+'_'+str(pos[1]//self.blocksize[1])+'[new_sheep]=pos')
      #1.0.2更新 这里也是用一个字典来存整个prey,优点在于删除的时间复杂度为1
      self.sheep_d[new_sheep] = pos


    for i in range(0, number_of_tiger):
      x = random.uniform(0,self.x_range)
      y = random.uniform(0,self.y_range)
      new_tiger = Tiger([int(x),int(y)])
      
      #这是目前我们的存储容器，字典
      #1.0.2更新，这里直接变成更新字典，应改为追加
      #exec('self.predator_'+str(int(x)//50)+'_'+str(int(y)//50)+'={new_tiger:[x,y]}')
      self.tiger_d[new_tiger] = [x,y]
      exec('self.tiger_'+str(int(x)//12)+'_'+str(int(y)//12)+'[new_tiger]=[x,y]')
  
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
      for Cow in self.cow_d.keys():
      # if Tiger.moveflag:
        pos=Cow.getPos()
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
        if self.dist < Cow.size+5: 
            #这个应该是牛（prey）移动到食物坐标，这里的move是原来的随机移动函数，我稍微改了一下，可能还有bug
            #这里应该还要调用eat函数，来更新牛吃到草后的属性更新
            #1.0.2更新，全局变量问题
            self.cow_d[Cow] = self.target_food_pos
            exec('self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Cow] = self.target_food_pos')
            Cow.move(self.target_food_pos)
            Cow.eat()
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
            Cow.random_move((self.x_range,self.y_range))
            exec('del self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Cow]')
            pos=Cow.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Cow] = pos')
            self.cow_d[Cow] = pos
      for Sheep in self.sheep_d.keys():
      # if Tiger.moveflag:
        pos=Sheep.getPos()
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
        if self.dist < Sheep.size+5: 
            #这个应该是牛（prey）移动到食物坐标，这里的move是原来的随机移动函数，我稍微改了一下，可能还有bug
            #这里应该还要调用eat函数，来更新牛吃到草后的属性更新
            #1.0.2更新，全局变量问题
            self.sheep_d[Sheep] = self.target_food_pos
            exec('self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] = self.target_food_pos')
            Sheep.move(self.target_food_pos)
            Sheep.eat()
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
            Sheep.random_move((self.x_range,self.y_range))
            exec('del self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep]')
            pos=Sheep.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] = pos')
            self.sheep_d[Sheep] = pos  
            
                
      #1.0.2更新，已经改了
      #这下面还没改，等上面牛吃草完善好了之后应该可以直接相同思路copy
      #1.0.2更新，for循环也改了，你们可以和原版比较一下
      for Tiger in self.tiger_d.keys():
      # if Tiger.moveflag:
        pos=Tiger.getPos()
        creatureXblock=pos[0]//self.blocksize[0]
        creatureYblock=pos[1]//self.blocksize[1]
        #1.0.2更新 变量更新
        self.dist = 999
        b = 'for Cow in self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_pos1 = self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Cow] \n  print(prey_pos1)\n  if self.dist > math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_pos1[0]-pos[0])**2+(prey_pos1[1]-pos[1])**2)\n    self.target_prey = Cow\n    self.target_prey_pos = prey_pos1'
      # if Tiger.moveflag:
        exec(b)
        b = 'for Sheep in self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+': \n  prey_s_pos1 = self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Sheep] \n  print(prey_s_pos1)\n  if self.dist > math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2): \n    self.dist = math.sqrt((prey_s_pos1[0]-pos[0])**2+(prey_s_pos1[1]-pos[1])**2)\n    self.target_prey = Sheep\n    self.target_prey_pos = prey_s_pos1'
        exec(b)
        #1.0.2更新 变量更新
        if self.dist < Tiger.size+5: 
            #这个应该是牛（prey）移动到食物坐标，这里的move是原来的随机移动函数，我稍微改了一下，可能还有bug
            #1.0.2更新 变量更新
            self.tiger_d[Tiger] = self.target_prey_pos
            exec('self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Tiger] = self.target_prey_pos')
            Tiger.move(self.target_prey_pos)
            Tiger.eat()
            #这是上一种思路，想通过食物的坐标反推其字典里面的key值，不过zip生成的是一次性的迭代器所以好像比较难操作，目前换了一种思路
            '''
            exec('temp = zip(self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'.values(), self.food_'+str(creatureXblock)+'_'+str(creatureYblock)+'.keys())')
            temp1 = temp[food_get_pos]
            '''
            #这一步是删除被吃的猎物（草）
            #1.0.2更新 除了删除对应50*50字典里的prey，还删除了存所有prey的字典：prey_d里面的prey
            if self.target_prey in self.cow_d:
              del self.cow_d[self.target_prey]
              exec('del self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_prey]')
            else:
              del self.sheep_d[self.target_prey]
              exec('del self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[self.target_prey]')

        #1.0.3更新 随机移动
        else:
            Tiger.random_move((self.x_range,self.y_range))
            exec('del self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Tiger]')
            pos=Tiger.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[Tiger] = pos')
            self.tiger_d[Tiger] = pos
        '''
        else:
            Tiger.random_move((self.x_range,self.y_range))
            '''
  #1.0.3更新 死亡迭代，繁殖迭代
  def reset_creatures(self):
    for cow in list(self.cow_d.keys()):
          #死亡
          if cow.health <100 or cow.life <= 0:   #似乎等价于creature.content不为false
            pos=cow.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            #从两个字典里面都要删除
            exec('del self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[cow]')
            del self.cow_d[cow]
          #繁殖  
          elif cow.fertility > 0:
            cow.life = cow.life-1
            p = Cow(cow.getPos(),cow.speed+np.random.randint(-10,10))
            pos = p.getPos()
            # print("New Cow added")
            self.cow_d[p] = pos
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.cow_'+str(creatureXblock)+'_'+str(creatureYblock)+'[p] = pos')
            cow.newIteration()
    
    for sheep in list(self.sheep_d.keys()):
          #死亡
          if sheep.health <100 or sheep.life <= 0:   #似乎等价于creature.content不为false
            pos=sheep.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            #从两个字典里面都要删除
            exec('del self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[sheep]')
            del self.sheep_d[sheep]
          #繁殖  
          elif sheep.fertility > 0:
            sheep.life = sheep.life-1
            p = Sheep(sheep.getPos(),sheep.speed+np.random.randint(-10,10))
            pos = p.getPos()
            # print("New Cow added")
            self.sheep_d[p] = pos
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.sheep_'+str(creatureXblock)+'_'+str(creatureYblock)+'[p] = pos')
            sheep.newIteration()
    
    # self.Cow = np.array(new_prey)
        
    for tiger in list(self.tiger_d.keys()):
          #死亡
          #print(tiger.health)
          if tiger.health <100 or tiger.life <= 0:   #似乎等价于creature.content不为false
            pos=tiger.getPos()
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            #从两个字典里面都要删除
            exec('del self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[tiger]')
            del self.tiger_d[tiger]
          #繁殖
          elif tiger.fertility > 0:
            tiger.life = tiger.life-1
            p = Tiger(tiger.getPos(),tiger.speed+np.random.randint(-10,10))
            pos = p.getPos()
            # print("New Cow added")
            self.tiger_d[p] = pos
            creatureXblock=pos[0]//self.blocksize[0]
            creatureYblock=pos[1]//self.blocksize[1]
            exec('self.tiger_'+str(creatureXblock)+'_'+str(creatureYblock)+'[p] = pos')
            tiger.newIteration()

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
        for Cow in self.cow_d:
            draw.circle(gameDisplay,Cow.color,Cow.getPos(),Cow.size+2)
        for Sheep in self.sheep_d:
            draw.circle(gameDisplay,Sheep.color,Sheep.getPos(),Sheep.size+2)
        for Tiger in self.tiger_d:
            draw.circle(gameDisplay,Tiger.color,Tiger.getPos(),Tiger.size-1)


    ##