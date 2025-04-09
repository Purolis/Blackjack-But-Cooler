from Deck import Deck
from Player import Player
from Dealer import Dealer
import os
import time


def main():
    # Creates a deck and shuffles the deck
    decklist = Deck([])
    decklist.create_deck()
    decklist.shuffle_deck()

    minimum_bet = 200

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
    # Creates player and dealer and sets base wealth to 1000

    global p1
    global p2
    global dealer
    # temp fix, refactor to not use global
    p1 = Player([], 0, None, 1000, starting_items)
    p2 = Dealer([], 0, "CPU1")
    dealer = Dealer([], 0, "Dealer")

    
    # Draws 2 cards for both the player and the dealer at the start
    clients = {
        "player": [p1, p2], 
        "dealer": dealer,
        }

    clients['player'][0].draw(decklist.draw_card())
    clients['player'][1].draw(decklist.draw_card())
    clients['dealer'].draw(decklist.draw_card())


    # Initializaes the actual game
    main_game_init(decklist, clients, minimum_bet)


def main_game_init(decklist, clients, min_bet):

    # Starting introduction
    print("Welcome to BlackJack!")
    time.sleep(0.5)

    running = True
    while running:

        # first bet
        bet_made = False
        while not bet_made:
            print("DEBUG:: betting1")
            bet = clients['player'][0].bet(min_bet)
            if bet == -1: 
                print("DEBUG:: not enough money, sell")
                # if a bet cannot be made, sell an item
                did_sell = clients['player'][0].sell_item()
                if did_sell == -1: 
                    print("DEBUG:: nothing to sell")
                    # no items to sell, game over
                    print("\n\n\tYou Lose!\n\tGame Over\n\tThank you for playing!\n")
                    exit()
                else:
                    continue
            else:
                print("DEBUG:: locked in bet")
                bet_made = True


            main_game_logic(clients, decklist, bet)
            time.sleep(1)
            for p in clients['player']:
                p.set_hand([])
            clients['dealer'].set_hand([])
            # p1.set_hand([])
            # p2.set_hand([])
            # dealer.set_hand([])

            # If the deck ever has no cards shuffle it
            if decklist.get_deck() is None:
                decklist.shuffle_deck()

            # Shows the current balance and deals a new hand
            print("Current Balance: $" + str(p1.get_player_wealth()))
            print("\nDealing new hand....")
            time.sleep(1)

            for x in range(2):
                for player in clients['player']:
                    player.draw(decklist.draw_card())
                clients['dealer'].draw(decklist.draw_card())


def main_game_logic(clients, decklist, bet):
    loop_boolean = False
    # While choice is still going
    while not loop_boolean:
        # os clears are just to make output look nice in command line,
        # os.system('cls' if os.name == 'nt' else 'clear')

        # Count's the hand value
        clients['player'][0].set_hand_value(clients['player'][0].count_hand())
        clients['player'][1].set_hand_value(clients['player'][1].count_hand())
        clients['dealer'].set_hand_value(dealer.count_hand())

        # If statements for game logic.
        if clients['dealer'].get_hand_value() != 21:
            while clients['player'][1].get_hand_value() < 17:
                clients['player'][1].draw(decklist.draw_card())
                clients['player'][1].set_hand_value(clients['player'][1].count_hand())
            display_player_cards(clients['player'][1].get_hand(), clients['player'][1].get_hand_value(), "P2")

            # If dealer doesn't have Blackjack, move forward and display the hands
            if clients['player'][0].get_hand_value() != 21 or clients['player'][0].get_hand_value() == 21 and len(clients['player'][0].get_hand()) > 2:
                print('Dealer Hand:')
                print(f'[{dealer.get_hand()[0].get_name()}]', end=' ')
                print(f'[]\n')
                display_player_cards(clients['player'][0].get_hand(), clients['player'][0].get_hand_value())
                user_choice = choice()

                # User input for stand or hit, if hit move forward
                if user_choice.upper() == 'H':

                    # Draw card and recount the hand and set it to the value.
                    clients['player'][0].draw(decklist.draw_card())
                    clients['player'][0].set_hand_value(clients['player'][0].count_hand())

                    # Game logic, if hand value is over 21 you lose automatically.
                    if clients['player'][0].get_hand_value() > 21:
                        # os.system('cls' if os.name == 'nt' else 'clear')
                        outcome(dealer, clients['player'][0], clients['player'][1], clients['player'][1].get_hand_value(),  dealer.get_hand_value(), clients['player'][0].get_hand_value(),
                                '\nYou busted, you lose!', 'lost', -bet)
                        loop_boolean = True

                else:
                    # Apart of the game logic it's just split up
                    loop_boolean = game_logic_split(
                        clients['dealer'], 
                        clients['player'][0], 
                        clients['player'][1], 
                        decklist, 
                        bet, 
                        loop_boolean
                    )

            else:
                # Game logic, you had 21 at the start from the beginning if statement!
                outcome(dealer, clients['player'][0], clients['player'][1], clients['player'][1].get_hand_value(),  dealer.get_hand_value(), clients['player'][0].get_hand_value(),
                        'You have Black jack, you win!',
                        'win ', bet)
                loop_boolean = True
        else:
            # Game logic, the dealer has black jack, you automatically lose no matter what.
            outcome(dealer, clients['player'][0], clients['player'][1], clients['player'][1].get_hand_value(), dealer.get_hand_value(), clients['player'][0].get_hand_value(),
                    'The dealer has Black jack, you lose!', 'lost', -bet)
            loop_boolean = True


# Function that neatly displays the cards in [example card] [example card]
def display_player_cards(hand, player_value, player='Your'):
    print(f'{player} Hand:')
    for card in hand:
        print(f'[{card.get_name()}]', end=' ')
    print(f'[Value: {player_value}]')


def dealer_17_logic(dealer, p1, p2, decklist):
    # Game logic, if the dealer has less than 17, and you stand, they MUST hit until over 17.
    while dealer.get_hand_value() < 17:
        time.sleep(1.5)
        # os.system('cls' if os.name == 'nt' else 'clear')

        dealer.draw(decklist.draw_card())
        dealer.set_hand_value(dealer.count_hand())

        # os.system('cls' if os.name == 'nt' else 'clear')
        display_player_cards(p2.get_hand(), p2.get_hand_value(), 'P2')
        print()
        display_player_cards(dealer.get_hand(), dealer.get_hand_value(), 'Dealer')
        print()
        display_player_cards(p1.get_hand(), p1.get_hand_value())


def game_logic_split(dealer, p1, p2, decklist, bet, loop_boolean):
    dealer_17_logic(dealer, p1, p2, decklist)
    # os.system('cls' if os.name == 'nt' else 'clear')

    # Game logic, if dealer's hand is over 21 while they are hitting they lose automatically.
    if dealer.get_hand_value() > 21:
        outcome(dealer, p1, p2, p2.get_hand_value(), dealer.get_hand_value(), p1.get_hand_value(),
                '\nDealer busts, you win!', 'won', bet)
        loop_boolean = True

    # Game logic, if you have a higher value than dealer at the end of all of this, you win!
    if p1.get_hand_value() > dealer.get_hand_value() and p1.get_hand_value() < 21:
        outcome(dealer, p1, p2, p2.get_hand_value(), dealer.get_hand_value(), p1.get_hand_value(),
                f'\n{p1.get_hand_value()} beats {dealer.get_hand_value()}, you win!', 'win', bet)

    # Game logic, if you have the same values, you push or tie.
    elif p1.get_hand_value() == dealer.get_hand_value():
        outcome(dealer, p1, p2, p2.get_hand_value(), dealer.get_hand_value(), p1.get_hand_value(),
                f'\n{p1.get_hand_value()} ties {dealer.get_hand_value()}, you push!', 'pushed', 0)

    # Game logic, if if dealer has more than you and is less than 21
    if p1.get_hand_value() < dealer.get_hand_value() and dealer.get_hand_value() < 21:
        # Game logic, else you will therefore have nothing but less than them so you lose.
        outcome(dealer, p1, p2, p2.get_hand_value(), dealer.get_hand_value(), p1.get_hand_value(),
                f'\n{p1.get_hand_value()} loses to {dealer.get_hand_value()}, you lose!', 'lost', -bet)
        loop_boolean = True
    return loop_boolean


def outcome(dealer, p1, p2, p2_value, dealer_value, p1_value, print_prompt, win_lose, bet):
    print()
    display_player_cards(p2.get_hand(), p2_value, 'P2')
    print()
    display_player_cards(dealer.get_hand(), dealer_value, 'Dealer')
    print()
    display_player_cards(p1.get_hand(), p1_value)
    print('\n', print_prompt)
    p1.set_player_wealth(p1.get_player_wealth() + bet)

    if p2_value > 21:
        print("P2 busts, he lost!")
    if p2_value < 21 and p1_value > dealer_value:
        print("P2 beats Dealer")
    if p2_value < 21 and p1_value < dealer_value:
        print("P2 loses to Dealer")
    if p2_value == dealer_value:
        print("P2 pushes to Dealer")

    print('\nYou', win_lose, str(bet), '! You now have $', p1.get_player_wealth(), 'dollars!')
    if p1.get_player_wealth() <= 0 and len(p1.get_items()) > 0:
        print(f'You are out of money. You need to sell something in order to continue playing! \n ')
        p1.sell_item()
        # item = input("Which item would you like to sell?")
        p1.print_item(item)


# Function that allows the user to bet and returns that bet
def user_bet(p1):
    print("")
    bets = int(input("How much would you like to bet: "))
    while bets > p1.get_player_wealth():
        print("You bet more money than you have. Please bet again!")
        bets = int(input("\nHow much would you like to bet: "))
    return bets


# Choice function that asks for hit or stand and return the choice given by user.
def choice():
    user = input('\nHit or Stand | Type H or S: ')
    boolean = True
    while boolean:

        # Try and catch in case the user does input something other than H or S.
        try:
            if user.upper() == 'H' or user.upper() == 'S':
                boolean = False
            else:
                user = input('Not a valid input | Type H or S: ')
        except:
            pass

    return user


if __name__ == '__main__':
    main()
