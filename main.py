'''
main.py
This is the main program of this project.You can run this file.
While True is the start of the loop.
1.The design of the initial interface GUI and the input of parameters from user.
2.Create world objects and generate various creatures in the world
3.Use a for loop to iterate over the number of days.
4.Use a while loop to iterate the action of creature within a day
5.Real-time display of the movement, death, and reproduction process of creatures, as well as drawing a line graph of the number of creatures.
'''


from numpy.core.numeric import ones
from numpy.lib.function_base import disp
import pygame
from pygame import *
from GUI import Button_TextBox_1_3
from GUI import gval
import numpy as np
import random
import numpy.linalg as LA
import math
import torch
from Tiger import Tiger
from Cow import Cow
from food import Food
from world import World 
from Sheep import Sheep
import matplotlib.backends.backend_agg as agg
import pylab
from evoluation.prey_nn import Prey_nn
from evoluation.predator_nn import Predator_nn
torch.cuda.set_device(0)
prey_net = Prey_nn(2,8,2)
prey_net.cuda(torch.device(0))
predator_net = Predator_nn(2,8,2)
predator_net.cuda(torch.device(0))
gval.init()

def main():
    clock = pygame.time.Clock()
    BT = Button_TextBox_1_3.Button_TextBox()
   
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
    button_2 = BT.button_2()
    button_3 = BT.button_3()
    
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
    BT.register_cp(button_2)
    BT.register_cp(button_3)
    BT.run(scr)

if __name__ == '__main__':
    main()
    
    pygame.quit()


# Function to plots the number of creature in the end of each day.
def plot_stats(gameDisplay,day_num,Tiger_num,Sheep_num,Cow_num,food_num):
  '''
  Function to add the plots of the number of creatures
  '''

  fig = pylab.figure(figsize=[4,4], dpi=100,)
  ax = fig.gca()
  ax.plot(day_num,Tiger_num,'k',label = "Tiger")
  ax.plot(day_num,Sheep_num,'r', label = "Sheep")
  ax.plot(day_num,Cow_num,'y',label = "Cow")
  ax.plot(day_num,food_num,'g',label = "Food")
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
  gameDisplay.blit(surf,(800,0))
  
  pygame.display.update()


while True:
    clock=time.Clock()
    '''
    h=600
    w=600
    gameDisplay=display.set_mode((h,w))
    display.set_caption("Evolution")
    '''
    w=1200
    h=800
    gameDisplay=display.set_mode((w,h))
    display.set_caption("Evolution")
    canvas = pygame.Surface((800,800))
    canvas_2 = pygame.Surface((400,400))
    canvas_3 = pygame.Surface((200,200))
    canvas_4 = pygame.Surface((400,200))
    main_plot = pygame.Rect(0,0,800,800)

    display.set_caption("Evolution")

    Sheeptats = []
    Tiger_stats = []

    # number_of_creatures =  int(gval.get_value("Creature Num"))
    # number_of_Cow
    # = 20*number_of_creatures
    # number_of_days = int(gval.get_value("Day Num"))
    # number_of_Tigers = number_of_creatures

    number_of_food = 1000
    number_of_Tigers = 5
    number_of_Cow = 100
    number_of_Sheep = 100
    number_of_forests = 12
    
    # number_of_Tigers = int(gval.get_value("Tiger Num"))
    # number_of_Cow = int(gval.get_value("Cow Num"))
    # number_of_Sheep = int(gval.get_value("Sheep Num"))
    # number_of_food = int(gval.get_value("Grass Num"))
    mode = gval.get_value("mode")
    forest_epicenters = [-1]*number_of_forests
    number_of_steps = 150
    number_of_days = 40

    pygame.init()
    
    sub_plot = pygame.Rect(0,0,600,600)
    text = pygame.Rect(0,0,200,200)
    myfont = pygame.font.Font(None,25)
    blue = (39,64,139)
    orange = (238,154,73)
    red = (205,85,85)
    textimage_1 = myfont.render("Initial Condition",True,orange)
    textimage_2 = myfont.render("Tiger Num:",True,orange)
    textimage_3 = myfont.render("Cow Num:",True,orange)
    textimage_4 = myfont.render("Sheep Num:",True,orange)
    textimage_5 = myfont.render("Gress Num:",True,orange)

    textimage_6 = myfont.render(str(number_of_Tigers),True,orange)
    textimage_7 = myfont.render(str(number_of_Cow),True,orange)
    textimage_8 = myfont.render(str(number_of_Sheep),True,orange)
    textimage_9 = myfont.render(str(number_of_food),True,orange)

    canvas_3.fill(blue)
    canvas_3.blit(textimage_1,(10,20))
    canvas_3.blit(textimage_2,(10,60))
    canvas_3.blit(textimage_3,(10,100))
    canvas_3.blit(textimage_4,(10,140))
    canvas_3.blit(textimage_5,(10,180))
    
    canvas_3.blit(textimage_6,(110,60))
    canvas_3.blit(textimage_7,(120,100))
    canvas_3.blit(textimage_8,(120,140))
    canvas_3.blit(textimage_9,(120,180))
    gameDisplay.blit(canvas_3,(1000,400))

    #Creature World object
    world = World()
    #Generate creature as what the user input
    world.initialize_creatures(number_of_Cow,number_of_Sheep,number_of_Tigers)

    Tiger_num = []
    Cow_num = []
    Sheep_num = []
    food_num = []
    day_num = []
    growthrate = 1

    #Start loop for one day
    for day in range(0,number_of_days):
        steps_taken = 0
        number_of_food = number_of_food-day*50*(growthrate-1)
        #Generate forest, which is the center of glass distribution.
        forest_epicenters = world.generate_food(number_of_food,len(forest_epicenters),forest_epicenters)
        canvas_2.fill((255,255,255))
        #Plot the number of each creature
        plot_stats(gameDisplay,day_num,Tiger_num,Sheep_num,Cow_num,food_num)
        #Randomly decide the weather today.
        climate = np.random.randint(0,3)
        while steps_taken < number_of_steps:
            #Tell which mode should the program conduct
            world.climate = climate
            if mode == 0:
                world.eat_and_move()
            else:
                p1,p2 = world.sensitive_eat_and_move(prey_net,predator_net)
                # print(p1)
                canvas_4.fill(blue)
                textimage_10 = myfont.render("Evoluation Level",True,red)
                textimage_11 = myfont.render("Tiger's avg Level:",True,red)
                textimage_12 = myfont.render("Cow's avg Level:",True,red)
                textimage_13 = myfont.render(str(p1[0]),True,red)
                textimage_14 = myfont.render(str(p2[0]),True,red)
                canvas_4.blit(textimage_10,(10,20))
                canvas_4.blit(textimage_11,(10,80))
                canvas_4.blit(textimage_12,(10,120))
                canvas_4.blit(textimage_13,(200,80))
                canvas_4.blit(textimage_14,(200,120))
                gameDisplay.blit(canvas_4,(800,600))
                display.update()
            #Half of a day had passed, it is night now!  
            if steps_taken < 75:
                    
                    if climate > 1: 
                        canvas.fill((139,115,85))
                        sunny = pygame.image.load('sunny.png')
                        sunny = pygame.transform.scale(sunny,(200,200))
                        gameDisplay.blit(sunny,(800,400))
                    else: 
                        canvas.fill((16,78,139))
                        rainy = pygame.image.load('rainy.png')
                        rainy = pygame.transform.scale(rainy,(200,200))
                        gameDisplay.blit(rainy,(800,400))
            else:
                canvas.fill((105,105,105))
                night = pygame.image.load('night.png')
                night = pygame.transform.scale(night,(200,200))
                gameDisplay.blit(night,(800,400))
            world.print_food(canvas)
            world.print_creatures(canvas)
            gameDisplay.blit(canvas,(0,0),main_plot)
            display.update()
            clock.tick(60)
            steps_taken = steps_taken + 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        #The loop for one day end, renew the number of each creature.
        Tiger_num.append(len(world.tiger_d))
        Cow_num.append(len(world.cow_d))
        Sheep_num.append(len(world.sheep_d))
        food_num.append(len(world.food_d))
        day_num.append(day+1)
        #After a day of activity, the creature reproduces or dies or spends the day normally
        world.reset_creatures()
        
        display.update()
        
        world.clear_food()
