import pygame 
from pygame.locals import *
from sys import exit
from GUI import gval

gval.init()
# from button.main import text_objects

pygame.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class Button_TextBox:

    def __init__(self, label_text = '',text = ''):
        
        self.title = "Start Screen"
        # 按钮部分
        self.button_title = "Start"
        self.button_size = 30
        self.button_pos = (300, 500)
        self.button_font = "freesansbold.ttf"
        self.button_fontc = (255, 255, 255)
        self.background = (55, 55, 55)
        self.button_clic_fc = (255, 255, 255)
        self.button_clic_bgc = (155, 155, 155)
        self.button_if_click = False
        self.button_crash_rect = [0,0,0,0]
        self.edge = 5
        self.width = 0
        # 标签部分
        self.label_font = "freesansbold.ttf"
        self.label_fontc = (100,100,255)
        ## 标签1
        self.label_title1 = "Creature Num"
        self.label_size1 = 30
        self.label_pos1 = (300,250)
        self.label_if_click1 = False
        self.label_crash_rect = [0,0,0,0]
        ## 标签2
        self.label_title2 = "Sim"
        self.label_size2 = 15
        self.label_pos2 = (100,100)
        self.label_if_click2 = False
        self.label_crash_rect2 = [0,0,0,0]
        ## 标签3
        self.label_title3 = "Creature Num"
        self.label_size3 = 15
        self.label_pos3 = (300,100)
        self.label_if_click3 = False
        self.label_crash_rect3 = [0,0,0,0]
        ## 标签4
        self.label_title4 = "Sim"
        self.label_size4 = 15
        self.label_pos4 = (500,100)
        self.label_if_click4 = False
        self.label_crash_rect4 = [0,0,0,0]
        ## 标签5
        self.label_title5 = "Sim"
        self.label_size5 = 15
        self.label_pos5 = (500,100)
        self.label_if_click5 = False
        self.label_crash_rect5 = [0,0,0,0]
        
        # 文本框部分
        self.box_font = "freesansbold.ttf"
        self.box_fontc = (100,0,255)
        ## 文本框1
        self.box_index1 = 1
        self.text1 = text
        self.box_color1 = COLOR_INACTIVE
        self.box_rect1 = pygame.Rect(1,1,1,1)
        self.txt_surface1 = FONT.render(text, True, self.box_fontc)
        self.box_if_click1 = False
        self.box_crash_rect1 = [0,0,0,0]
        ## 文本框2
        self.box_index2 = 1
        self.text2 = text
        self.box_color2 = COLOR_INACTIVE
        self.box_rect2 = pygame.Rect(1,1,1,1)
        self.txt_surface2 = FONT.render(text, True, self.box_fontc)
        self.box_if_click2 = False
        self.box_crash_rect2 = [0,0,0,0]
        ## 文本框3
        self.box_index3 = 1
        self.text3 = text
        self.box_color3 = COLOR_INACTIVE
        self.box_rect3 = pygame.Rect(1,1,1,1)
        self.txt_surface3 = FONT.render(text, True, self.box_fontc)
        self.box_if_click3 = False
        self.box_crash_rect3 = [0,0,0,0]

        ## 文本框4
        self.box_index4 = 1
        self.text4 = text
        self.box_color4 = COLOR_INACTIVE
        self.box_rect4 = pygame.Rect(1,1,1,1)
        self.txt_surface4 = FONT.render(text, True, self.box_fontc)
        self.box_if_click4 = False
        self.box_crash_rect4 = [0,0,0,0]
        
        


        
        self.size = (600,600)
        self.comp = []
    
    def init(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        return screen

    def listening(self):
        x, y = pygame.mouse.get_pos()
        for m in self.comp:
            if m[1][0] <= x <= m[1][0]+m[1][2] \
                and m[1][1] <= y <= m[1][3]+m[1][1]:
                m[2] = True
            else:
                m[2] = False


    def button(self):
        return["bu", self.button_crash_rect, self.button_if_click]

    def label1(self, title, pos):
        self.label_title1 = title
        self.label_pos1 = pos
        return ["la1", self.label_crash_rect2, self.label_if_click2]

    def label2(self, title, pos):
        self.label_title2 = title
        self.label_pos2 = pos
        return ["la2", self.label_crash_rect2, self.label_if_click2]

    def label3(self, title, pos):
        self.label_title3 = title
        self.label_pos3 = pos
        return ["la3", self.label_crash_rect3, self.label_if_click3]

    def label4(self, title, pos):
        self.label_title4 = title
        self.label_pos4 = pos
        return ["la4", self.label_crash_rect4, self.label_if_click4]
    
    def label5(self, title, pos):
        self.label_title5 = title
        self.label_pos5 = pos
        return ["la5", self.label_crash_rect5, self.label_if_click5]

    def box1(self, x, y, w, h, index):
        self.box_index1 = index
        self.box_rect1 = pygame.Rect(x,y,w,h)
        return ["box1", self.box_crash_rect1, self.box_if_click1, index]

    def box2(self, x, y, w, h, index):
        self.box_index2 = index
        self.box_rect2 = pygame.Rect(x,y,w,h)
        return ["box2", self.box_crash_rect2, self.box_if_click2, index]

    def box3(self, x, y, w, h, index):
        self.box_index3 = index
        self.box_rect3 = pygame.Rect(x,y,w,h)
        return ["box3", self.box_crash_rect3, self.box_if_click3, index]
    def box4(self, x, y, w, h, index):
        self.box_index4 = index
        self.box_rect4 = pygame.Rect(x,y,w,h)
        return ["box4", self.box_crash_rect4, self.box_if_click4, index]

    def register_cp(self,way):
        self.comp.append(way)

    def label1_text_objects(self, font):
        text_surface = font.render(self.label_title1, True, self.label_fontc)
        return text_surface, text_surface.get_rect()

    def label2_text_objects(self, font):
        text_surface = font.render(self.label_title2, True, self.label_fontc)
        return text_surface, text_surface.get_rect()

    def label3_text_objects(self, font):
        text_surface = font.render(self.label_title3, True, self.label_fontc)
        return text_surface, text_surface.get_rect()

    def label4_text_objects(self, font):
        text_surface = font.render(self.label_title4, True, self.label_fontc)
        return text_surface, text_surface.get_rect()
    def label5_text_objects(self, font):
        text_surface = font.render(self.label_title5, True, self.label_fontc)
        return text_surface, text_surface.get_rect()
    
    def box1_text_objects(self, font):
        text_surface = font.render(self.text1, True, self.box_fontc)
        return text_surface, text_surface.get_rect()

    def box2_text_objects(self, font):
        text_surface = font.render(self.text2, True, self.box_fontc)
        return text_surface, text_surface.get_rect()

    def box3_text_objects(self, font):
        text_surface = font.render(self.text3, True, self.box_fontc)
        return text_surface, text_surface.get_rect()
    
    def box5_text_objects(self, font):
        text_surface = font.render(self.text5, True, self.box_fontc)
        return text_surface, text_surface.get_rect()
    
    def button_text_objects(self, font):
        text_surface = font.render(self.button_title, True, self.button_fontc)
        return text_surface, text_surface.get_rect()

    def display(self, scr):
        for n in self.comp:
            if n[0] == "bu":
                if n[2]:
                    large_text = pygame.font.Font(self.button_font, self.button_size)
                    text_surf, text_rect = self.button_text_objects(large_text)
                    text_rect.center = self.button_pos
                    pygame.draw.rect(scr, self.background, (text_rect.left - self.edge,
                                                 text_rect.top - self.edge,
                                                 text_rect.width + self.edge*2,
                                                 text_rect.height + self.edge*2), self.width)
                    scr.blit(text_surf, text_rect)
                    n[1] = text_rect
                else:
                    large_text = pygame.font.Font(self.button_font, self.button_size)
                    text_surf, text_rect = self.button_text_objects(large_text)
                    text_rect.center = self.button_pos
                    pygame.draw.rect(scr, self.background, (text_rect.left - self.edge,
                                                            text_rect.top - self.edge,
                                                            text_rect.width + self.edge*2,
                                                            text_rect.height + self.edge*2), self.width)
                    scr.blit(text_surf,text_rect)
                    n[1] = text_rect
            if n[0] == "la1":
                large_text = pygame.font.Font(self.label_font, self.label_size1)
                text_surf, text_rect = self.label1_text_objects(large_text)
                text_rect.center = self.label_pos1
                if self.background != 0:
                    pygame.draw.rect(scr, self.background, (text_rect.left-self.edge,
                                                 text_rect.top-self.edge,
                                                 text_rect.width+self.edge*2,
                                                 text_rect.height+self.edge*2), self.edge)
                scr.blit(text_surf, text_rect)

            if n[0] == "la2":
                large_text = pygame.font.Font(self.label_font, self.label_size2)
                text_surf, text_rect = self.label2_text_objects(large_text)
                text_rect.center = self.label_pos2
                if self.background != 0:
                    pygame.draw.rect(scr, self.background, (text_rect.left-self.edge,
                                                 text_rect.top-self.edge,
                                                 text_rect.width+self.edge*2,
                                                 text_rect.height+self.edge*2), self.edge)
                scr.blit(text_surf, text_rect)

            if n[0] == "la3":
                large_text = pygame.font.Font(self.label_font, self.label_size3)
                text_surf, text_rect = self.label3_text_objects(large_text)
                text_rect.center = self.label_pos3
                if self.background != 0:
                    pygame.draw.rect(scr, self.background, (text_rect.left-self.edge,
                                                 text_rect.top-self.edge,
                                                 text_rect.width+self.edge*2,
                                                 text_rect.height+self.edge*2), self.edge)
                scr.blit(text_surf, text_rect)

            if n[0] == "la4":
                large_text = pygame.font.Font(self.label_font, self.label_size4)
                text_surf, text_rect = self.label4_text_objects(large_text)
                text_rect.center = self.label_pos4
                if self.background != 0:
                    pygame.draw.rect(scr, self.background, (text_rect.left-self.edge,
                                                 text_rect.top-self.edge,
                                                 text_rect.width+self.edge*2,
                                                 text_rect.height+self.edge*2), self.edge)
                scr.blit(text_surf, text_rect)
            
            if n[0] == "la5":
                large_text = pygame.font.Font(self.label_font, self.label_size5)
                text_surf, text_rect = self.label5_text_objects(large_text)
                text_rect.center = self.label_pos5
                if self.background != 0:
                    pygame.draw.rect(scr, self.background, (text_rect.left-self.edge,
                                                 text_rect.top-self.edge,
                                                 text_rect.width+self.edge*2,
                                                 text_rect.height+self.edge*2), self.edge)
                scr.blit(text_surf, text_rect)
                
            
            
            if n[0] == "box1":
                
                    scr.blit(self.txt_surface1, (self.box_rect1.x+5, self.box_rect1.y+5))
                    pygame.draw.rect(scr, self.box_color1, self.box_rect1, 2)

            if n[0] == "box2":
                
                    scr.blit(self.txt_surface2, (self.box_rect2.x+5, self.box_rect2.y+5))
                    pygame.draw.rect(scr, self.box_color2, self.box_rect2, 2)

            if n[0] == "box3":
                
                    scr.blit(self.txt_surface3, (self.box_rect3.x+5, self.box_rect3.y+5))
                    pygame.draw.rect(scr, self.box_color3, self.box_rect3, 2)
            
            if n[0] == "box4":
                
                    scr.blit(self.txt_surface4, (self.box_rect4.x+5, self.box_rect4.y+5))
                    pygame.draw.rect(scr, self.box_color4, self.box_rect4, 2)
                    
            
            
    
    def run(self,scr):
        go_on = True
        while go_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    go_on = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 265<= mouse_x and mouse_x<= 335 and 485 <=  mouse_y and mouse_y <= 515:
                        gval.set_value("Tiger Num", self.text1)
                        gval.set_value("Sheep Num", self.text2)
                        gval.set_value("Cow Num", self.text3)
                        gval.set_value("Glass Num", self.text4)
                        go_on = False
                    if self.box_rect1.collidepoint(event.pos):
                        self.box_if_click1 = not self.box_if_click1
                    else:
                        self.box_if_click1 = False

                    if self.box_rect2.collidepoint(event.pos):
                        self.box_if_click2 = not self.box_if_click2
                    else:
                        self.box_if_click2 = False

                    if self.box_rect3.collidepoint(event.pos):
                        self.box_if_click3 = not self.box_if_click3
                    else:
                        self.box_if_click3 = False
                    if self.box_rect4.collidepoint(event.pos):
                        self.box_if_click4 = not self.box_if_click4
                    else:
                        self.box_if_click4 = False
                    self.box_color1 = COLOR_ACTIVE if self.box_if_click1 else COLOR_INACTIVE
                    self.box_color2 = COLOR_ACTIVE if self.box_if_click2 else COLOR_INACTIVE
                    self.box_color3 = COLOR_ACTIVE if self.box_if_click3 else COLOR_INACTIVE
                    self.box_color4 = COLOR_ACTIVE if self.box_if_click3 else COLOR_INACTIVE
                elif event.type ==  KEYDOWN:
                    
                    if self.box_if_click1:
                        if event.key == K_RETURN:
                            # gval.set_value("Creature Num", self.text1)
                            # # print(self.text1)
                            self.text1 = ''
                        elif event.key == K_BACKSPACE:
                            self.text1 = self.text1[:-1]
                        
                        else:
                            self.text1 += event.unicode
                        self.txt_surface1 = FONT.render(self.text1, True, self.box_fontc)

                    if self.box_if_click2:
                        if event.key == K_RETURN:
                            # gval.set_value("Food Num", self.text2)
                            # # print(self.text2)
                            self.text2 = ''
                        elif event.key == K_BACKSPACE:
                            self.text2 = self.text2[:-1]
                        else:
                            self.text2 += event.unicode
                        self.txt_surface2 = FONT.render(self.text2, True, self.box_fontc)
                    
                    if self.box_if_click3:
                        if event.key == K_RETURN:
                            # gval.set_value("Day Num", self.text3)
                            # # print(self.text3)
                            self.text3 = ''
                        elif event.key == K_BACKSPACE:
                            self.text3 = self.text3[:-1]
                        else:
                            self.text3 += event.unicode
                        self.txt_surface3 = FONT.render(self.text3, True, self.box_fontc)
                    
                    if self.box_if_click4:
                        if event.key == K_RETURN:
                            # gval.set_value("Day Num", self.text3)
                            # # print(self.text3)
                            self.text4 = ''
                        elif event.key == K_BACKSPACE:
                            self.text4 = self.text4[:-1]
                        else:
                            self.text4 += event.unicode
                        self.txt_surface4 = FONT.render(self.text4, True, self.box_fontc)



            scr.fill(self.background)
            self.display(scr)
            self.listening()
            pygame.display.update()



