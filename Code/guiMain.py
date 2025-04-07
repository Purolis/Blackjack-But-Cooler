# This driver is for testing; eventually the GUI will be implemented into main.py

import pygame, sys
from Button import Button

# pygame initialization
pygame.init()
pygame.display.set_caption("Blackjack++")

# constants
SCREEN = pygame.display.set_mode((1500, 1000))
UI_FONT = pygame.font.Font('assets/Lullaby-Strange.otf',35)
SCR_WIDTH = SCREEN.get_width()
SCR_HEIGHT = SCREEN.get_height()
COLORS = {
    # pre-set colors for reduced duplication
    "black": (0,0,0),
    "white": (255,255,255),
    "red": (255,0,0),
    "green": (0,255,0),
    "blue": (0,0,255),
}

# UI elements
buttons = {
    "btn1": Button (
        width=250,
        height=100,
        pos_x=300,
        pos_y=250,
        text="QUIT",
        font=UI_FONT,
        color_bg=COLORS["white"],
        color_text=COLORS["red"],
        # image=None,
        # event=None,
    ),
    "btn2": Button (
        width=150,
        height=50,
        pos_x=50,
        pos_y=200,
        text="START",
        font=UI_FONT,
        color_bg=COLORS["green"],
        color_text=COLORS["black"],
        # image=None,
        # event=None,
    ),
}

# how to handle images; put this into class method
img = pygame.image.load("assets/Flat-Playing-Cards-Set/Spades/A.png")



# game loop
running = True
while running:
    # stores the (x,y) coordinates of mouse position into the variable as a tuple
    mouse_pos = pygame.mouse.get_pos()

    # event handling
    #   right now, the only "event" is closing the game.
    #   TODO: *proper* event handling logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
             # if the mouse_pos is clicked on the button the game is terminated
             for btn in buttons.keys():
                if buttons[btn].get_pos_x() <= mouse_pos[0] <= (buttons[btn].get_pos_x() + buttons[btn].get_width()) and \
                            buttons[btn].get_pos_y() <= mouse_pos[1] <= (buttons[btn].get_pos_y() + buttons[btn].get_height()):
                            # 🡹🡹 check if mouse_pos X and Y positions are within button bounds 🡹🡹
                    running = False
                    # add event handling here;
                            # btn.get_event()

    # rendering game elements
    for btn in buttons.keys():
        buttons[btn].render_button(SCREEN)

    # how to handle images; put this into class render method
    SCREEN.blit(img, (700, 20))

    # push frame to screen
    pygame.display.update()

# stop execution gracefully
pygame.quit()
sys.exit()