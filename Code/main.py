from Deck import Deck
from Player import Player
from Dealer import Dealer
from Money import Money
import os
import time


def main():
    decklist = Deck()
    decklist.create_deck()
    decklist.shuffle_deck()

    p1 = Player()
    dealer = Dealer()
    players = [p1, dealer]
# - Money should be a Player data attribute; makes it extensible
    cash = Money(50)
    player_wealth = cash.get_player_wealth()

    for x in range(2):
        for player in players:
            player.draw(decklist.draw_card())

    while True:
        # clear the terminal output to simplify the display (makes current state more obvious)
        os.system('cls' if os.name == 'nt' else 'clear')

        # p1_value = p1.count_hand()
        # dealer_value = dealer.count_hand()
# - why not just use p1.count_hand() ? 
#           unnecessary variables is confusing, can lead to logic errors
#           use get_hand_value() instead of count_hand()

        if dealer.count_hand() != 21:
            if p1.count_hand() != 21 or p1.count_hand() == 21 and len(p1.get_hand()) > 2:
# - make "Their hand" the name of the player e.g. "Dealer", "You"
                print('Dealer Hand:')
                print(f'[{dealer.get_hand()[0].get_name()}]', end=' ')
                print(f'[]\n')
                display_player_cards(p1.get_hand(), p1.count_hand())
                user_choice = user_prompt()

                if user_choice.upper() == 'H':
                    p1.draw(decklist.draw_card())

                    if p1.count_hand() > 21:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        display_player_cards(dealer.get_hand(), dealer.count_hand(), 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1.count_hand())
                        print('\nYou busted, you lose!')
                        player_wealth -= 50
                        cash.set_player_wealth(player_wealth)
                        print('\nYou lost $50 Dollars! You now have $', player_wealth, 'dollars!\n')
                        print("You lost all your money! You lose at life!")

                        break

                else:
                    while dealer.count_hand() < 17:
                        time.sleep(1.5)
                        os.system('cls' if os.name == 'nt' else 'clear')

                        dealer.draw(decklist.draw_card())

                        os.system('cls' if os.name == 'nt' else 'clear')
                        display_player_cards(dealer.get_hand(), dealer.count_hand, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1.count_hand())

                    os.system('cls' if os.name == 'nt' else 'clear')
                    if dealer.count_hand() > 21:
                        display_player_cards(dealer.get_hand(), dealer.count_hand, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1.count_hand())
                        print('\nDealer busts, you win!')
                        player_wealth += 50
                        cash.set_player_wealth(player_wealth)

                        print('\nYou won $50 Dollars! You now have $', player_wealth, 'dollars!')
                        break

                    if p1.count_hand() > dealer.count_hand:
                        display_player_cards(dealer.get_hand(), dealer.count_hand, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1.count_hand())
                        print(f'\n{p1.count_hand()} beats {dealer.count_hand}, you win!')
                    elif p1.count_hand() == dealer.count_hand:
                        display_player_cards(dealer.get_hand(), dealer.count_hand, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1.count_hand())
                        print(f'\n{p1.count_hand()} ties {dealer.count_hand}, you push!')
                    else:
                        display_player_cards(dealer.get_hand(), dealer.count_hand, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1.count_hand())
                        print(f'\n{p1.count_hand()} loses to {dealer.count_hand}, you lose!')
                        player_wealth -= 50
                        cash.set_player_wealth(player_wealth)
                        print('\nYou lost $50 Dollars! You now have $', player_wealth, 'dollars!\n')
                        print("You lost all your money! You lose at life!")

                    break
            else:
                display_player_cards(dealer.get_hand(), dealer.count_hand, 'Their')
                print()
                display_player_cards(p1.get_hand(), p1.count_hand())
                print('\nYou have Black Jack, you win!')
                player_wealth += 50
                cash.set_player_wealth(player_wealth)

                print('\nYou won $50 Dollars! You now have $', player_wealth, 'dollars!')
                break
        else:
            display_player_cards(dealer.get_hand(), dealer.count_hand, 'Their')
            print()
            display_player_cards(p1.get_hand(), p1.count_hand())
            print('\nThe dealer has Black Jack, you lose!')
            player_wealth -= 50
            cash.set_player_wealth(player_wealth)
            print('\nYou lost $50 Dollars! You now have $', player_wealth, 'dollars!\n')
            print("You lost all your money! You lose at life!")
            break


def display_player_cards(hand, player_value, player='Your'):
    print(f'{player} Hand:')
    for card in hand:
        print(f'[{card.get_name()}]', end=' ')
    print(f'[Value: {player_value}]')


def user_prompt():
    # refactor to be universal, just a validator
    # parameters: valid_chars[]
    user_choice = input('\nHit or Stand | Type H or S: ')

    valid_entry = False
    while not valid_entry:
        try:
            if user_choice.upper() == 'H' or user_choice.upper() == 'S':
                valid_entry = True
            else:
                user_choice = input('Not a valid input | Type H or S: ')
        except: # extend this, what errors
            pass

    return user_choice


if __name__ == '__main__':
    main()
