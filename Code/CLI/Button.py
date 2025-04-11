# TODO: refactor according to: UML_UI_diagram.drawio

import pygame

class Button:
    __width:int = -1
    __height:int = -1
    __pos_x:int = -1
    __pos_y:int = -1
    __text:str = "None"
    __font = None
    __color_bg:tuple = (255,255,255)
    __color_text:tuple = (0,0,0)
    # __image = None
    # __event = None

    def __init__(self, width, height, pos_x, pos_y, text, font, color_bg, color_text): #image, event
        """
        :param width the horizontal length of the button from the top-left corner.
        :param height the vertical length of the button from the top-left corner.
        :param pos_x horizontal position of top-left corner of button.
        :param pos_y vertical position of top-left corner of button.
        :param color_bg background color of the button.
        :param color_text text color of the button.
        """
        self.set_width(width)
        self.set_height(height)
        self.set_pos_x(pos_x)
        self.set_pos_y(pos_y)
        self.set_text(text)
        self.set_font(font)
        self.set_color_bg(color_bg)
        self.set_color_text(color_text)
        #set image
        #set event

    ### helpers
    def render_button(self, screen): # called in game loop
        pygame.font.init()
        text = self.get_font().render(self.get_text(), True, self.get_color_text())
        
        # button background
        pygame.draw.rect(screen, self.get_color_bg(), [self.get_pos_x(), self.get_pos_y(), self.get_width(), self.get_height()])
        
        # overlay text on top of rect, centered on rect
        screen.blit(text, (self.get_pos_x()+(self.get_width()/2)-(text.get_width()/2), self.get_pos_y()+(self.get_height()/2)-(text.get_height()/2)))

    ### getters
    def get_width(self):
        return self.__width
    def get_height(self):
        return self.__height
    def get_pos_x(self):
        return self.__pos_x
    def get_pos_y(self):
        return self.__pos_y
    def get_text(self):
        return self.__text
    def get_font(self):
        return self.__font
    def get_color_bg(self):
        return self.__color_bg
    def get_color_text(self):
            return self.__color_text
    #get image
    #get event

    ### setters
    def set_width(self, width):
        self.__width = width
    def set_height(self, height):
        self.__height = height
    def set_pos_x(self, pos_x):
        self.__pos_x = pos_x
    def set_pos_y(self, pos_y):
        self.__pos_y = pos_y
    def set_text(self, text):
        self.__text = text
    def set_font(self, font):
        self.__font = font
    def set_color_bg(self, color_bg):
        self.__color_bg = color_bg
    def set_color_text(self, color_text):
        self.__color_text = color_text
    #set image
    #set event

    ### to_string
    def __str__(self):
        txt = "Button description:\n"
        txt += "\twidth: " + str(self.get_width()) + "\n"
        txt += "\theight: " + str(self.get_height()) + "\n"
        txt += "\tpos x: " + str(self.get_pos_x()) + "\n"
        txt += "\tpos y: " + str(self.get_pos_y()) + "\n"
        txt += "\ttext: " + str(self.get_text()) + "\n"
        txt += "\tcolor bg: " + str(self.get_color_bg()) + "\n"
        txt += "\tcolor text: " + str(self.get_color_text()) + "\n"
        return txt