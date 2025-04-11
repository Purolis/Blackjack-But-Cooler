# TODO: This driver is for testing; eventually the GUI will be implemented into main.py

import pygame, sys
from Button import Button
from Deck import Deck
from Player import Player
from Dealer import Dealer
import time

# pygame initialization
pygame.init()
pygame.display.set_caption("Blackjack++")
info = pygame.display.Info()
scr_w = info.current_w
scr_h = info.current_h

# constants
SCREEN = pygame.display.set_mode((scr_w, scr_h), pygame.FULLSCREEN)
UI_FONT = pygame.font.Font('assets/Lullaby-Strange.otf', 35)
SCR_WIDTH = SCREEN.get_width()
SCR_HEIGHT = SCREEN.get_height()
COLORS = {
    # pre-set colors for reduced duplication
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}

dealer_h = SCR_HEIGHT*0.05
player_h = SCR_HEIGHT*0.75

starting_items = {
        "house": 50_000,
        "firstborn": 30_000,
        "car": 25_000,
        "dog": 666,
        "watch": 500,
        "shoes": 90,
        "pants": 50,
        "shirt": 15,
    }

minimum_bet = 200
decklist = Deck([])


def main():
    home_screen()

    # Creates players and dealer and sets base wealth to 1000
    p1 = Player([], 0, None, 1000, starting_items)
    dealer = Dealer([], 0, "Dealer")

    clients = {
        "player": p1,
        "dealer": dealer,
    }

    # Initializes the actual game
    while True:

        clients['player'].set_hand([])
        clients['dealer'].set_hand([])

        decklist.create_deck()
        decklist.shuffle_deck()

        for x in range(2):
            clients['player'].draw(decklist.draw_card())
            clients['dealer'].draw(decklist.draw_card())

        main_game_init(decklist, clients, minimum_bet)

        again = gui_input('WANT TO PLAY ANOTHER HAND? TYPE Y OR N: ')

        while True:
            if again.upper() == 'N':
                clear_screen()
                exit_thanks = create_text('THANK YOU FOR PLAYING!', COLORS['white'])
                render_surface(exit_thanks, (SCR_WIDTH / 2 - exit_thanks.get_width() / 2, SCR_HEIGHT / 2 - exit_thanks.get_height() / 2))
                update()
                time.sleep(2)

                pygame.quit()
                sys.exit()
            elif again.upper() == 'Y':
                break
            else:
                again = gui_input('NOT A VALID INPUT, TYPE Y OR N: ')


def home_screen():
    # UI elements
    buttons = {
        "btn1": Button(
            width=SCR_WIDTH/12,
            height=SCR_HEIGHT/12,
            pos_x=SCR_WIDTH/2+SCR_WIDTH/24,
            pos_y=SCR_HEIGHT/2+SCR_HEIGHT/8,
            text="QUIT",
            font=UI_FONT,
            color_bg=COLORS["white"],
            color_text=COLORS["red"],
            # image=None,
            # event=None,
        ),
        "btn2": Button(
            width=SCR_WIDTH/12,
            height=SCR_HEIGHT/12,
            pos_x=SCR_WIDTH/2-SCR_WIDTH/8,
            pos_y=SCR_HEIGHT/2+SCR_HEIGHT/8,
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
    img_w, img_h = img.get_size()

    running = True
    while running:
        # stores the (x,y) coordinates of mouse position into the variable as a tuple
        mouse_pos = pygame.mouse.get_pos()

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the mouse_pos is clicked on the button the game is terminated
                for btn in buttons.keys():
                    if buttons[btn].get_pos_x() <= mouse_pos[0] <= (buttons[btn].get_pos_x() + buttons[btn].get_width()) and \
                        buttons[btn].get_pos_y() <= mouse_pos[1] <= (buttons[btn].get_pos_y() + buttons[btn].get_height()):
                        # 🡹🡹 check if mouse_pos X and Y positions are within button bounds 🡹🡹
                        if buttons[btn].get_text() == 'QUIT':
                            running = False
                            pygame.quit()
                            sys.exit()
                        else:
                            running = False
                            # TODO: add event handling here;
                            # btn.get_event()

            # rendering game elements
            for btn in buttons.keys():
                buttons[btn].render_button(SCREEN)

            text = UI_FONT.render('WELCOME TO BLACKJACK', True, COLORS['white'])

            # TODO: this is how to handle images; put this into class render method
            SCREEN.blit(img, (SCR_WIDTH/2 - img_w/2, SCR_HEIGHT/2 - img_h))
            SCREEN.blit(text, (SCR_WIDTH/2-text.get_width()/2, SCR_HEIGHT/2+text.get_height()/2))

            # push frame to screen
            pygame.display.update()


def clear_screen():
    SCREEN.fill((0, 0, 0))


# coor is short for coordinates
def render_surface(surface, coor):
    SCREEN.blit(surface, coor)


def update():
    pygame.display.flip()


def create_card_img(card, override=False, path=None):
    if not override:
        temp = pygame.image.load(card.get_img())
    else:
        temp = pygame.image.load(path)
    return pygame.transform.scale_by(temp, 1/3)


def create_text(text, color):
    return UI_FONT.render(text, True, color)


def gui_input(input_prompt):

    choice = ''
    clear_screen()
    prompt = create_text(input_prompt, COLORS['white'])
    render_surface(prompt, (SCR_WIDTH/2-prompt.get_width()/2, SCR_HEIGHT/2-prompt.get_height()/2))
    update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    choice = choice[:-1]
                    print(choice)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    return choice
                else:
                    choice += event.unicode.upper()

                clear_screen()

                temp = create_text(choice, COLORS['white'])

                prompt_w = SCR_WIDTH/2-(prompt.get_width()+temp.get_width())/2
                temp_w = prompt_w+prompt.get_width()+15
                height = SCR_HEIGHT/2-temp.get_height()/2

                render_surface(temp, (temp_w, height))
                render_surface(prompt, (prompt_w, height))
                update()


def display_hand(player, height, dealer=False):
    hand = []
    total_hand_width = 0

    if not dealer:
        for card in player.get_hand():
            hand.append(create_card_img(card))

    else:
        hand.append(create_card_img(player.get_hand()[0]))
        hand.append(create_card_img(None, True, 'assets/Flat-Playing-Cards-Set/Back-Covers/Pomegranate.png'))

    for card in hand:
        total_hand_width += card.get_width()

    alignment = total_hand_width/2

    for card in hand:
        render_surface(card, (SCR_WIDTH/2-alignment, height))
        alignment -= card.get_width()+15

    if not dealer:
        hand_count = create_text(f'HAND TOTAL: {player.get_hand_value()}', COLORS['white'])
    else:
        hand_count = create_text(f'HAND TOTAL: ?', COLORS['white'])
    render_surface(hand_count, (SCR_WIDTH/2-hand_count.get_width()/2, height+hand[0].get_height()+10))

    update()


def display_full_board(clients, dealer=True):
    display_hand(clients['dealer'], dealer_h, dealer)
    display_hand(clients['player'], player_h)

    enter_prompt = create_text('CLICK ENTER TO CONTINUE...', COLORS['white'])
    render_surface(enter_prompt, (SCR_WIDTH/2-enter_prompt.get_width()/2, SCR_HEIGHT/2-enter_prompt.get_height()/2))
    update()

    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    loop = False


def enter_wait(x, y):

    prompt = create_text('PRESS ENTER TO CONTINUE...', COLORS['white'])
    render_surface(prompt, (x-prompt.get_width()/2, y))
    update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    return 0


def main_game_init(decklist, clients, min_bet):

    # first bet
    bet_made = False
    while not bet_made:

        clear_screen()
        money = create_text('YOU HAVE ' + str(clients['player'].get_player_wealth()) + ' DOLLARS!', COLORS['white'])
        render_surface(money, (SCR_WIDTH / 2 - money.get_width() / 2, SCR_HEIGHT / 2 - money.get_height() / 2))
        update()
        time.sleep(2)

        if clients['player'].get_player_wealth() >= min_bet:

            input = gui_input('HOW MUCH WOULD YOU LIKE TO BET: ')

            while True:
                try:
                    input = int(input)
                    break
                except:
                    input = gui_input('THAT WAS NOT A VALID INTEGER BET: ')

            bet = clients['player'].bet(min_bet, input)

            if bet == 1:
                clear_screen()
                temp = create_text('YOU CAN\'T BET MORE THAN YOU HAVE!', COLORS['white'])
                render_surface(temp, (SCR_WIDTH/2-temp.get_width()/2, SCR_HEIGHT/2-temp.get_height()/2))
                update()
                time.sleep(2)
            elif bet == 2:
                clear_screen()
                temp = create_text(f'YOU HAVE TO BET AT LEAST {min_bet} DOLLARS!', COLORS['white'])
                render_surface(temp, (SCR_WIDTH / 2 - temp.get_width() / 2, SCR_HEIGHT / 2 - temp.get_height() / 2))
                update()
                time.sleep(2)
            else:

                clear_screen()
                bet_confirm = create_text(f'YOU BET {input} DOLLARS!', COLORS['white'])
                render_surface(bet_confirm, (SCR_WIDTH/2-bet_confirm.get_width()/2, SCR_HEIGHT/2-bet_confirm.get_height()/2))
                update()
                time.sleep(2)

                bet = int(input)
                bet_made = True

                main_game_logic(clients, decklist, bet)

        else:
            clear_screen()
            no_money = create_text('YOU DON\'T HAVE ENOUGH MONEY, SELL SOME ITEMS', COLORS['white'])
            render_surface(no_money, (SCR_WIDTH / 2 - no_money.get_width() / 2, SCR_HEIGHT / 2 - no_money.get_height() / 2))
            update()
            time.sleep(2)

            selling = True
            while selling:
                # if a bet cannot be made, sell an item
                did_sell = sell_item_gui(clients['player'])
                if did_sell == -1:
                    clear_screen()
                    lose = create_text('GAME OVER!', COLORS['red'])
                    render_surface(lose, (SCR_WIDTH / 2 - lose.get_width() / 2, SCR_HEIGHT / 2 - lose.get_height() / 2))
                    update()
                    time.sleep(2)

                    clear_screen()
                    lose = create_text('THANKS FOR PLAYING!', COLORS['white'])
                    render_surface(lose, (SCR_WIDTH / 2 - lose.get_width() / 2, SCR_HEIGHT / 2 - lose.get_height() / 2))
                    update()
                    time.sleep(2)

                    pygame.quit()
                    sys.exit()

                if clients['player'].get_player_wealth() < min_bet:
                    clear_screen()
                    no_money = create_text('YOU STILL DON\'T HAVE ENOUGH MONEY, SELL MORE!!!!', COLORS['white'])
                    render_surface(no_money, (SCR_WIDTH/2-no_money.get_width()/2, SCR_HEIGHT/2-no_money.get_height()/2))
                    update()
                    time.sleep(2)
                else:
                    clear_screen()
                    gamble = create_text('YOU CAN FINALLY GAMBLE AGAIN! WHO NEEDS MONEY ANYWAY?', COLORS['white'])
                    render_surface(gamble, (SCR_WIDTH/2-gamble.get_width()/2, SCR_HEIGHT/2-gamble.get_height()/2))
                    update()
                    time.sleep(2)

                    bet_made = True
                    selling = False
    return 0


def main_game_logic(clients, decklist, bet):
    loop_boolean = False
    # While choice is still going
    while not loop_boolean:

        # Count's the hand value
        clients['player'].set_hand_value(clients['player'].count_hand())
        clients['dealer'].set_hand_value(clients['dealer'].count_hand())

        # If statements for game logic.
        if clients['dealer'].get_hand_value() != 21:

            # If dealer doesn't have Blackjack, move forward and display the hands
            if clients['player'].get_hand_value() != 21 or clients['player'].get_hand_value() == 21 and len(
                    clients['player'].get_hand()) > 2:

                clear_screen()
                display_full_board(clients)

                clear_screen()
                user_choice = gui_input('HIT OR STAND. HAND TOTAL IS ' + str(clients['player'].get_hand_value()) + ' TYPE H OR S: ')

                while True:
                    if user_choice.upper() == 'H' or user_choice.upper() == 'S':
                        break
                    else:
                        user_choice = gui_input('NOT A VALID INPUT, TYPE H OR S: ')

                # User input for stand or hit, if hit move forward
                if user_choice.upper() == 'H':

                    # Draw card and recount the hand and set it to the value.
                    clients['player'].draw(decklist.draw_card())
                    clients['player'].set_hand_value(clients['player'].count_hand())

                    # Game logic, if hand value is over 21 you lose automatically.
                    if clients['player'].get_hand_value() > 21:

                        clear_screen()
                        display_full_board(clients, False)
                        outcome(clients, 'YOU BUSTED, YOU LOSE!', 'LOST', -bet)
                        loop_boolean = True
                else:
                    # Apart of the game logic it's just split up
                    game_logic_split(clients, decklist, bet)
                    loop_boolean = True
            else:
                # Game logic, you had 21 at the start from the beginning if statement!
                clear_screen()
                display_full_board(clients, False)
                outcome(clients, 'YOU HAVE BLACK JACK, YOU WIN!', 'WIN ', bet)
                loop_boolean = True
        else:
            # Game logic, the dealer has black jack, you automatically lose no matter what.
            clear_screen()
            display_full_board(clients, False)
            outcome(clients, 'THE DEALER HAS BLACK JACK, YOU LOSE!', 'LOST', -bet)
            loop_boolean = True

    return 0


def dealer_17_logic(clients, decklist):
    clear_screen()
    display_full_board(clients, False)

    # Game logic, if the dealer has less than 17, and you stand, they MUST hit until over 17.
    while clients['dealer'].get_hand_value() < 17:
        # os.system('cls' if os.name == 'nt' else 'clear')

        clients['dealer'].draw(decklist.draw_card())
        clients['dealer'].set_hand_value(clients['dealer'].count_hand())

        clear_screen()
        display_full_board(clients, False)

    return 0


def game_logic_split(clients, decklist, bet):
    dealer_17_logic(clients, decklist)

    # Game logic, if dealer's hand is over 21 while they are hitting they lose automatically.
    if clients['dealer'].get_hand_value() > 21:
        outcome(clients, 'DEALER BUSTS, YOU WIN!', 'WON', bet)

    # Game logic, if you have a higher value than dealer at the end of all of this, you win!
    elif clients['player'].get_hand_value() > clients['dealer'].get_hand_value():
        outcome(clients, 'YOU WIN!', 'WON', bet)

    # Game logic, if you have the same values, you push or tie.
    elif clients['player'].get_hand_value() == clients['dealer'].get_hand_value():
        outcome(clients, f'{clients['player'].get_hand_value()} TIES {clients['dealer'].get_hand_value()}, YOU PUSH!', 'PUSHED', 0)

    # Game logic, if dealer has more than you and is less than 21
    elif clients['player'].get_hand_value() < clients['dealer'].get_hand_value():
        # Game logic, else you will therefore have nothing but less than them so you lose.
        outcome(clients, f'{clients['player'].get_hand_value()} LOSES TO {clients['dealer'].get_hand_value()}, YOU LOSE!', 'LOST', -bet)

    return 0


def sell_item_gui(client):
    """
    returns 0 for successful item sell; -1 for "unable to sell"
    """
    # check for empty inventory
    if client.get_items() == {}:

        clear_screen()
        no_money = create_text('YOU HAVE NO ITEMS TO SELL!', COLORS['white'])
        render_surface(no_money, (SCR_WIDTH/2-no_money.get_width()/2, SCR_HEIGHT/2-no_money.get_height()/2))
        time.sleep(2)

        return -1  # error code, no items to sell, tell game to quit

    else:
        # display options to player
        clear_screen()
        sell_opts = create_text('CHOOSE FROM BELOW WHICH ITEM TO SELL. TYPE THE FULL NAME OF THE ITEM', COLORS['white'])

        alignment = sell_opts.get_height()

        item_list = [sell_opts]
        for i in client.get_items():

            items = create_text(f'{str(i.title()).upper()}: {str(client.get_value(i))}', COLORS['white'])
            item_list.append(items)
            alignment += items.get_height()

        choice = ''
        input = True
        while input:

            prompt = create_text('CHOICE: ', COLORS['white'])
            temp = create_text(choice, COLORS['white'])

            prompt_w = SCR_WIDTH / 2 - (prompt.get_width() + temp.get_width()) / 2
            temp_w = prompt_w + prompt.get_width() + 15
            clear_screen()

            keep_align = alignment/2
            for item in item_list:
                render_surface(item, (SCR_WIDTH/2-item.get_width()/2, SCR_HEIGHT/2-keep_align))
                keep_align -= item.get_height()+15

            render_surface(temp, (temp_w, SCR_HEIGHT/2-keep_align))
            render_surface(prompt, (prompt_w, SCR_HEIGHT/2-keep_align))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        choice = choice[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:

                        # input validation for player selection
                        valid_choice = choice
                        valid = True

                        for char in valid_choice:
                            try:
                                char = int(char)
                                valid = False
                                clear_screen()
                                not_valid = create_text('THAT WAS NOT A VALID CHOICE!', COLORS['white'])
                                render_surface(not_valid, (SCR_WIDTH/2-not_valid.get_width()/2, SCR_HEIGHT/2-not_valid.get_height()/2))
                                update()
                                time.sleep(2)
                                break
                            except:
                                pass

                        if valid_choice.lower() in starting_items and valid:
                            input = False
                        elif valid:
                            clear_screen()
                            not_valid = create_text('THAT WAS NOT A VALID CHOICE!', COLORS['white'])
                            render_surface(not_valid, (SCR_WIDTH / 2 - not_valid.get_width() / 2, SCR_HEIGHT / 2 - not_valid.get_height() / 2))
                            update()
                            time.sleep(2)
                    else:
                        choice += event.unicode.upper()

            update()

        choice = choice.lower()

        # update player wealth and items
        new_items = client.get_items()
        gained_wealth = new_items[choice]
        client.set_player_wealth(client.get_player_wealth() + gained_wealth)

        clear_screen()
        new_money = create_text(f'GAINED WEALTH: {str(gained_wealth)}', COLORS['white'])
        render_surface(new_money, (SCR_WIDTH/2-new_money.get_width()/2, SCR_HEIGHT/2-new_money.get_height()/2))

        del (new_items[choice])
        client.set_items(new_items)

        new_wealth = create_text(f'NEW WEALTH TOTAL: {client.get_player_wealth()}', COLORS['white'])
        render_surface(new_wealth, (SCR_WIDTH/2-new_wealth.get_width()/2, SCR_HEIGHT/2+new_wealth.get_height()+15))
        update()
        time.sleep(2)

        return 0  # ran without issue


def outcome(clients, print_prompt, win_lose, bet):

    clear_screen()
    outcome_text = create_text(print_prompt.upper(), COLORS['white'])
    render_surface(outcome_text, (SCR_WIDTH/2-outcome_text.get_width()/2, SCR_HEIGHT/2-outcome_text.get_height()/2))
    update()
    time.sleep(2)

    clients['player'].set_player_wealth(clients['player'].get_player_wealth() + bet)

    clear_screen()
    win_lose_text = create_text('YOU ' + str(win_lose) + ' ' + str(abs(bet)) + '! YOU NOW HAVE ' + str(clients['player'].get_player_wealth()) + ' DOLLARS!', COLORS['white'])
    render_surface(win_lose_text, (SCR_WIDTH/2-win_lose_text.get_width()/2, SCR_HEIGHT/2-win_lose_text.get_height()/2))
    update()
    time.sleep(2)

    return 0


if __name__ == '__main__':
    main()
