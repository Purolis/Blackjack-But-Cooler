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

    # Creates player and dealer and sets base wealth to 1000
    p1 = Player([], 0, 1000)
    dealer = Dealer([], 0)
    players = [p1, dealer]
    player_wealth = p1.get_player_wealth()

    # Draws 2 cards for both the player and the dealer at the start
    for x in range(2):
        for player in players:
            player.draw(decklist.draw_card())

    # While choice is still going
    while True:
        # os clears are just to make output look nice in command line,
        os.system('cls' if os.name == 'nt' else 'clear')

        # Count's the hand value
        p1_value = p1.count_hand()
        dealer_value = dealer.count_hand()

        # If statements for game logic.
        if dealer_value != 21:

            # If dealer doesn't have Blackjack, move forward and display the hands
            if p1_value != 21 or p1_value == 21 and len(p1.get_hand()) > 2:
                print('Their Hand:')
                print(f'[{dealer.get_hand()[0].get_name()}]', end=' ')
                print(f'[]\n')
                display_player_cards(p1.get_hand(), p1_value)
                user_choice = choice()

                # User input for stand or hit, if hit move forward
                if user_choice.upper() == 'H':

                    # Draw card and recount the hand and set it to the value.
                    p1.draw(decklist.draw_card())
                    p1_value = p1.count_hand()

                    # Game logic, if hand value is over 21 you lose automatically.
                    if p1_value > 21:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        display_player_cards(dealer.get_hand(), dealer_value, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1_value)
                        print('\nYou busted, you lose!')
                        player_wealth -= 50
                        p1.set_player_wealth(player_wealth)
                        print('\nYou lost $50 Dollars! You now have $', player_wealth, 'dollars!\n')
                        print("You lost all your money! You lose at life!")

                        break

                else:

                    # Game logic, if the dealer has less than 17, and you stand, they MUST hit until over 17.
                    while dealer_value < 17:
                        time.sleep(1.5)
                        os.system('cls' if os.name == 'nt' else 'clear')

                        dealer.draw(decklist.draw_card())
                        dealer_value = dealer.count_hand()

                        os.system('cls' if os.name == 'nt' else 'clear')
                        display_player_cards(dealer.get_hand(), dealer_value, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1_value)

                    os.system('cls' if os.name == 'nt' else 'clear')

                    # Game logic, if dealer's hand is over 21 while they are hitting they lose automatically.
                    if dealer_value > 21:
                        display_player_cards(dealer.get_hand(), dealer_value, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1_value)
                        print('\nDealer busts, you win!')
                        player_wealth += 50
                        p1.set_player_wealth(player_wealth)

                        print('\nYou won $50 Dollars! You now have $', player_wealth, 'dollars!')
                        break

                    # Game logic, if you have a higher value than dealer at the end of all of this, you win!
                    if p1_value > dealer_value:
                        display_player_cards(dealer.get_hand(), dealer_value, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1_value)
                        print(f'\n{p1_value} beats {dealer_value}, you win!')

                    # Game logic, if you have the same values, you push or tie.
                    elif p1_value == dealer_value:
                        display_player_cards(dealer.get_hand(), dealer_value, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1_value)
                        print(f'\n{p1_value} ties {dealer_value}, you push!')
                    else:

                        # Game logic, else you will therefore have nothing but less than them so you lose.
                        display_player_cards(dealer.get_hand(), dealer_value, 'Their')
                        print()
                        display_player_cards(p1.get_hand(), p1_value)
                        print(f'\n{p1_value} loses to {dealer_value}, you lose!')
                        player_wealth -= 50
                        p1.set_player_wealth(player_wealth)
                        print('\nYou lost $50 Dollars! You now have $', player_wealth, 'dollars!\n')
                        print("You lost all your money! You lose at life!")

                    break
            else:

                # Game logic, you had 21 at the start from the beginning if statement!
                display_player_cards(dealer.get_hand(), dealer_value, 'Their')
                print()
                display_player_cards(p1.get_hand(), p1_value)
                print('\nYou have Black Jack, you win!')
                player_wealth += 50
                p1.set_player_wealth(player_wealth)

                print('\nYou won $50 Dollars! You now have $', player_wealth, 'dollars!')
                break
        else:

            # Game logic, the dealer has black jack, you automatically lose no matter what.
            display_player_cards(dealer.get_hand(), dealer_value, 'Their')
            print()
            display_player_cards(p1.get_hand(), p1_value)
            print('\nThe dealer has Black Jack, you lose!')
            player_wealth -= 50
            p1.set_player_wealth(player_wealth)
            print('\nYou lost $50 Dollars! You now have $', player_wealth, 'dollars!\n')
            print("You lost all your money! You lose at life!")
            break


# Function that neatly displays the cards in [example card] [example card]
def display_player_cards(hand, player_value, player='Your'):
    print(f'{player} Hand:')
    for card in hand:
        print(f'[{card.get_name()}]', end=' ')
    print(f'[Value: {player_value}]')


# Choice function that asks for hit or stand and return the choice given by user.
def choice():
    user = input('\nHit or Stand | Type H or S: ')
    while True:

        # Try and catch in case the user does input something other than H or S.
        try:
            if user.upper() == 'H' or user.upper() == 'S':
                break
            else:
                user = input('Not a valid input | Type H or S: ')
        except:
            pass

    return user


if __name__ == '__main__':
    main()
