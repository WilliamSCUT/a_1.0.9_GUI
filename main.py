from numpy.core.numeric import ones
import pygame
from pygame import *
from GUI import Button_TextBox_1_2
from GUI import gval
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
from food import Food
from world import World 
from Sheep import Sheep
import matplotlib.backends.backend_agg as agg
import pylab


gval.init()

def main():
    clock = pygame.time.Clock()
    BT = Button_TextBox_1_2.Button_TextBox()
   
    scr = BT.init()
    input_box1 = BT.box1(25, 300, 100, 30, 1)
    input_box2 = BT.box2(170, 300, 100, 30, 2)
    input_box3 = BT.box3(325, 300, 100, 30, 2)
    input_box4 = BT.box4(475, 300, 100, 30, 2)
    
    label_1 = BT.label1("Ecosystem Simulator",(300,100))
    label_2 = BT.label2("Tiger Num",(70,250))
    label_3 = BT.label3("Sheep Num",(220,250))
    label_4 = BT.label4("Cow Num",(370,250))
    label_5 = BT.label5("Grass Num",(520,250))
    button = BT.button()
    
    BT.register_cp(input_box1)
    BT.register_cp(input_box2)
    BT.register_cp(input_box3)
    BT.register_cp(input_box4)
    
    BT.register_cp(label_1)
    BT.register_cp(label_2)
    BT.register_cp(label_3)
    BT.register_cp(label_4)
    BT.register_cp(label_5)
    BT.register_cp(button)
    BT.run(scr)

if __name__ == '__main__':
    main()
    
    pygame.quit()

# 以上是开始界面，用来输入参数

def plot_stats(gameDisplay,day_num,Tiger_num,Sheep_num,Cow_num,food_num):
  '''
  Function to add the plots of the number of creatures
  '''

  fig = pylab.figure(figsize=[3,3], dpi=100,)
  ax = fig.gca()
  ax.plot(day_num,Tiger_num,label = "Tiger")
  ax.plot(day_num,Sheep_num, label = "Sheep")
  ax.plot(day_num,Cow_num,label = "Cow")
  ax.plot(day_num,food_num,label = "Food")
  ax.legend()
  
  ax.set_xlabel("Day Number")

  ax.set_title("Creature Status")
  ax.grid()
  
  canvas_2 = agg.FigureCanvasAgg(fig)
  canvas_2.draw()
  renderer = canvas_2.get_renderer()
  raw_data = renderer.tostring_rgb()
  size = canvas_2.get_width_height()

  surf = pygame.image.fromstring(raw_data,size,"RGB")
  gameDisplay.blit(surf,(600,0))
  
  pygame.display.update()
  
while True:
    clock=time.Clock()
    '''
    h=600
    w=600
    gameDisplay=display.set_mode((h,w))
    display.set_caption("Evolution")
    '''
    w=900
    h=600
    gameDisplay=display.set_mode((w,h))
    display.set_caption("Evolution")
    canvas = pygame.Surface((600,600))
    canvas_2 = pygame.Surface((300,300))
    main_plot = pygame.Rect(0,0,600,600)
    sub_plot = pygame.Rect(0,0,300,300)
    # 定义屏幕

    #接下来是主程序部分

    #展示屏幕

    display.set_caption("Evolution")

    Sheeptats = []
    Tiger_stats = []
    # number_of_creatures =  int(gval.get_value("Creature Num"))
    # number_of_Cow
    # = 20*number_of_creatures
    # number_of_days = int(gval.get_value("Day Num"))
    # number_of_Tigers = number_of_creatures

    number_of_food = 1000
    number_of_Tigers = 10
    number_of_Cow = 100
    number_of_Sheep = 100
    number_of_forests = 7
    # number_of_food = int(gval.get_value("Food Num"))
    number_of_steps = 150
    forest_epicenters = [-1]*number_of_forests

    number_of_days = 100
    #这个只执行一次
    world = World()
    world.initialize_creatures(number_of_Cow,number_of_Sheep,number_of_Tigers)

    Tiger_num = []
    Cow_num = []
    Sheep_num = []
    food_num = []
    day_num = []

    for day in range(0,number_of_days):
    #Sheeptats.append(world.num_Cow
    #)
        canvas_2.fill((255,255,255))
        Tiger_num.append(len(world.tiger_d))
        Cow_num.append(len(world.cow_d))
        Sheep_num.append(len(world.sheep_d))
        food_num.append(len(world.food_d))
        day_num.append(day+1)
        plot_stats(gameDisplay,day_num,Tiger_num,Sheep_num,Cow_num,food_num)

        steps_taken = 0
        forest_epicenters = world.generate_food(number_of_food,len(forest_epicenters),forest_epicenters)
        climate = np.random.randint(0,9)
        while steps_taken < number_of_steps:
            
            world.eat_and_move()
            steps_taken = steps_taken + 1
            world.print_food(canvas)
            world.print_creatures(canvas)
            
            gameDisplay.blit(canvas,(0,0),main_plot)
            
            display.update()
            clock.tick(60)
            if steps_taken < 75:
                    
                    if climate <5: # 晴天
                        canvas.fill((255,255,255))
                        sunny = pygame.image.load('sunny.png')
                        sunny = pygame.transform.scale(sunny,(200,200))
                        gameDisplay.blit(sunny,(600,300))
                    else: # 雨天
                        canvas.fill((30,144,255))
                        rainy = pygame.image.load('rainy.png')
                        rainy = pygame.transform.scale(rainy,(200,200))
                        gameDisplay.blit(rainy,(600,300))
            else:
                canvas.fill((105,105,105))
                night = pygame.image.load('night.png')
                night = pygame.transform.scale(night,(200,200))
                gameDisplay.blit(night,(600,300))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        world.reset_creatures()
        world.clear_food()
    
    # GUI
    
 
##接下来的部分大家可以理解后按照顺序补充



'''
def addGrass(_num):
    for i in range(_num):
        x = np.random.randint(0, size) # 0到size是x的上下限，没有给size默认为1
        y = np.random.randint(0, size)
        while grid[x][y] != 0:
            x = np.random.randint(0, size)
            y = np.random.randint(0, size)

        grid[x][y] = 1  # 1代表草


def addGrassEater(_num):
    for i in range(_num):
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)
        while grid[x][y] != 0:
            x = np.random.randint(0, size)
            y = np.random.randint(0, size)

        grid[x][y] = 2  # 2代表食草动物


def addMeatEater(_num):
    for i in range(_num):
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)
        while grid[x][y] != 0 or growAround(x, y, 2) == [-1, -1]:
            x = np.random.randint(0, size)
            y = np.random.randint(0, size)

        grid[x][y] = 3  # 3代表食肉动物


def growAround(_x, _y, _id):
    field = []
    if _x-1 < 0:
        x_begin = 0
    else:
        x_begin = _x-1
    if _y-1 < 0:
        y_begin = 0
    else:
        y_begin = _y-1
    if _x+1 > size-1:
        x_end = size-1
    else:
        x_end = _x+1
    if _y+1 > size-1:
        y_end = size-1
    else:
        y_end = _y+1

    for i in range(x_begin, x_end+1):
        for j in range(y_begin, y_end+1):
            if grid[i][j] == _id or grid[i][j] == _id*10:  # 2代表食草动物，1代表草，0代表空地
                field += [[i, j]]

    if len(field) == 0:  # 没有食物或者空地
        return [-1, -1]
    else:
        count = np.random.randint(0, len(field))
        return field[count]


def fieldUpdate():
    for i in range(size):
        for j in range(size):
            if grid[i][j] == 30:
                grid[i][j] = 3
            elif grid[i][j] == 20:
                grid[i][j] = 2
            elif grid[i][j] == 10:
                grid[i][j] = 1


def data_gen():
    for count in range(times):
        timesText.set_text('times: %d' % (count+1))
        for i in range(size):
            for j in range(size):
                if grid[i][j] == 3:
                    place = growAround(i, j, 2)
                    if place == [-1, -1]:
                        grid[i][j] = 0  # 食肉动物死亡
                    else:
                        grid[i][j] = 0
                        grid[place[0]][place[1]] = 30  # 食肉动物进食并移动
                        growth = growAround(i, j, 0)
                        if growth != [-1, -1]:
                            grid[growth[0]][growth[1]] = 30  # 食肉动物繁殖

                if grid[i][j] == 2:
                    place = growAround(i, j, 1)
                    if place == [-1, -1]:
                        grid[i][j] = 0  # 食草动物死亡
                    else:
                        grid[i][j] = 0
                        grid[place[0]][place[1]] = 20  # 食草动物进食并移动
                        growth = growAround(i, j, 0)
                        if growth != [-1, -1]:
                            grid[growth[0]][growth[1]] = 20  # 食草动物繁殖

                elif grid[i][j] == 1:
                    growth = growAround(i, j, 0)
                    if growth != [-1, -1]:
                        grid[growth[0]][growth[1]] = 10  # 草生长

        fieldUpdate()

        yield grid


def update(_data):
    ax.imshow(_data, interpolation='nearest', cmap='Set3', norm=norm)
    return ax
'''
'''
times = 100  # 迭代次数
size = 40
grid = np.zeros((size, size))  # 0代表空地
addGrass(1200)
addGrassEater(150)
addMeatEater(30)

fig = plt.figure()
ax = plt.subplot(111)
norm = matplotlib.colors.Normalize(vmin=0, vmax=3)  # 固定数值对应的颜色映射
gci = ax.imshow(grid, interpolation='nearest', cmap='Set3', norm=norm)
ax.set_xticks([])
ax.set_yticks([])
cbar = plt.colorbar(gci)
cbar.set_ticks(np.linspace(0, 3, 4))
cbar.set_ticklabels(('Space', 'Grass', 'GrassEater', 'MeatEater'))
timesText = plt.text(-2, -2, 'times: 0')
ani = animation.FuncAnimation(
    fig, update, data_gen, interval=1000, repeat=False)

plt.show()
'''
