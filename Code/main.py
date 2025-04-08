from Deck import Deck
from Player import Player
from Dealer import Dealer
import os
import time

# NOTE: THIS IS BROKEN, RUN test.py TO SEE WHAT I'M DOING
# NOTE: THIS IS BROKEN, RUN test.py TO SEE WHAT I'M DOING
# NOTE: THIS IS BROKEN, RUN test.py TO SEE WHAT I'M DOING
# NOTE: THIS IS BROKEN, RUN test.py TO SEE WHAT I'M DOING
# NOTE: THIS IS BROKEN, RUN test.py TO SEE WHAT I'M DOING
# NOTE: THIS IS BROKEN, RUN test.py TO SEE WHAT I'M DOING
# NOTE: THIS IS BROKEN, RUN test.py TO SEE WHAT I'M DOING
# NOTE: THIS IS BROKEN, RUN test.py TO SEE WHAT I'M DOING
# NOTE: THIS IS BROKEN, RUN test.py TO SEE WHAT I'M DOING

def main():
    # Creates a deck and shuffles the deck
    decklist = Deck([])
    decklist.create_deck()
    decklist.shuffle_deck()

    # Creates player and dealer and sets base wealth to 1000
    p1 = Player([], 0, 1000, {"Dog": 750, "Car": 500, "House":2000 })
    dealer = Dealer([], 0)

    # Draws 2 cards for both the player and the dealer at the start
    players = [p1, dealer]
    for x in range(2):
        for player in players:
            player.draw(decklist.draw_card())

    print("Welcome to BlackJack!")
    time.sleep(1)
    while p1.get_player_wealth() > 0:
        bet = user_bet(p1)
        time.sleep(1.5)
        game_logic(p1, dealer, decklist, bet)
        time.sleep(1.5)
        p1.set_hand([])
        dealer.set_hand([])
        if decklist.get_deck() is None:
            decklist.shuffle_deck()

        for x in range(2):
            for player in players:
                player.draw(decklist.draw_card())




def game_logic(p1, dealer, decklist, bet):
    loop_boolean = False
    # While choice is still going
    while not loop_boolean:
        # os clears are just to make output look nice in command line,
        os.system('cls' if os.name == 'nt' else 'clear')

        # Count's the hand value
        p1.set_hand_value(p1.count_hand())
        dealer.set_hand_value(p1.count_hand())

        # If statements for game logic.
        if dealer.get_hand_value() != 21:

            # If dealer doesn't have Blackjack, move forward and display the hands
            if p1.get_hand_value() != 21 or p1.get_hand_value() == 21 and len(p1.get_hand()) > 2:
                print('Their Hand:')
                print(f'[{dealer.get_hand()[0].get_name()}]', end=' ')
                print(f'[]\n')
                display_player_cards(p1.get_hand(), p1.get_hand_value())
                user_choice = choice()

                # User input for stand or hit, if hit move forward
                if user_choice.upper() == 'H':

                    # Draw card and recount the hand and set it to the value.
                    p1.draw(decklist.draw_card())
                    p1.set_hand_value(p1.count_hand())

                    # Game logic, if hand value is over 21 you lose automatically.
                    if p1.get_hand_value() > 21:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        outcome(dealer, p1, dealer.get_hand_value(), p1.get_hand_value(),
                                '\nYou busted, you lose!', 'lost', -bet)
                        loop_boolean = True

                else:

                    # Game logic, if the dealer has less than 17, and you stand, they MUST hit until over 17.
                    while dealer.get_hand_value() < 17:
                        time.sleep(1.5)
                        os.system('cls' if os.name == 'nt' else 'clear')

                        dealer.draw(decklist.draw_card())
                        dealer.set_hand_value(dealer.count_hand())

                        os.system('cls' if os.name == 'nt' else 'clear')
                        display_player_cards(dealer.get_hand(), dealer.get_hand_value(), 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1.get_hand_value())

                    os.system('cls' if os.name == 'nt' else 'clear')

                    # Game logic, if dealer's hand is over 21 while they are hitting they lose automatically.
                    if dealer.get_hand_value() > 21:
                        outcome(dealer, p1, dealer.get_hand_value(), p1.get_hand_value(),
                                '\nDealer busts, you win!', 'won', bet)
                        loop_boolean = True

                    # Game logic, if you have a higher value than dealer at the end of all of this, you win!
                    if p1.get_hand_value() > dealer.get_hand_value() and p1.get_hand_value() < 21:
                        outcome(dealer, p1, dealer.get_hand_value(), p1.get_hand_value(),
                                f'\n{p1.get_hand_value()} beats {dealer.get_hand_value()}, you win!', 'win', bet)

                    # Game logic, if you have the same values, you push or tie.
                    elif p1.get_hand_value() == dealer.get_hand_value():
                        outcome(dealer, p1, dealer.get_hand_value(), p1.get_hand_value(),
                                f'\n{p1.get_hand_value()} ties {dealer.get_hand_value()}, you push!', 'pushed', 0)
                    if p1.get_hand_value() < dealer.get_hand_value() and dealer.get_hand_value() < 21:

                        # Game logic, else you will therefore have nothing but less than them so you lose.
                        outcome(dealer, p1, dealer.get_hand_value(), p1.get_hand_value(),
                                f'\n{p1.get_hand_value()} loses to {dealer.get_hand_value()}, you lose!', 'lost', -bet)
                        loop_boolean = True
            else:
                # Game logic, you had 21 at the start from the beginning if statement!
                outcome(dealer, p1, dealer.get_hand_value(), p1.get_hand_value(),
                        'You have Black jack, you win!',
                        'win ', bet)
                loop_boolean = True
        else:
            # Game logic, the dealer has black jack, you automatically lose no matter what.
            outcome(dealer, p1, dealer.get_hand_value(), p1.get_hand_value(),
                    'The dealer has Black jack, you lose!', 'lost', -bet)
            loop_boolean = True


# Function that neatly displays the cards in [example card] [example card]
def display_player_cards(hand, player_value, player='Your'):
    print(f'{player} Hand:')
    for card in hand:
        print(f'\t[{card.get_name()}]', end='\n')
    print(f'[Hand Value: {player_value}]')



def outcome(dealer, p1, dealer_value, p1_value, print_prompt, win_lose, bet):
    display_player_cards(dealer.get_hand(), dealer_value, 'Their')
    print()
    display_player_cards(p1.get_hand(), p1_value)
    print('\n', print_prompt)
    p1.set_player_wealth(p1.get_player_wealth() + bet)

    print('\nYou',win_lose, str(bet), '! You now have $',p1.get_player_wealth(),'dollars!')
    if p1.get_player_wealth() <= 0 and len(p1.get_items()) > 0:
        print(f'You are out of money. You need to sell something in order to continue playing! \n ')
        print(f'You have these items available to sell:\n {p1.get_items()}')
        item = input("Which item would you like to sell?")
        p1.print_item(item)



def user_bet(p1):
    print("")
    bets = int(input("\nHow much would you like to bet?"))
    while bets > p1.get_player_wealth():
        print("You bet more money than you have. Please bet again!")
        bets = int(input("\nHow much would you like to bet?"))
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
