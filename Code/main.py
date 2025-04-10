# I decided to overhaul main.py
# This runs, but isn't fully functional
# I wasn't happy with our code whatsoever, so I've taken what I've learnt and coded until my brain melted and dribbled out my ears
# I hope this makes sense and is expandable! I think this will be much easier to eventually give a GUI to.
# I have been in the weeds here for a while, so it might be more confusing than I think it is
#   - Nova

from Deck import Deck
from Player import Player
from Dealer import Dealer
from enum import Enum
import os
import time

def main():
# greet user
    print("""\n\n
██████████████████████████████████████████████████████████████████████████████████████████████████████████████ 
██████████████████████████████████████████████████████████████████████████████████████████████████████████████
██                                                                                                          ██
██  ▀█████████▄   ▄█          ▄████████  ▄████████    ▄█   ▄█▄      ▄█    ▄████████  ▄████████    ▄█   ▄█▄  ██
██    ███    ███ ███         ███    ███ ███    ███   ███ ▄███▀     ███   ███    ███ ███    ███   ███ ▄███▀  ██
██    ███    ███ ███         ███    ███ ███    █▀    ███▐██▀       ███   ███    ███ ███    █▀    ███▐██▀    ██
██   ▄███▄▄▄██▀  ███         ███    ███ ███         ▄█████▀        ███   ███    ███ ███         ▄█████▀     ██
██  ▀▀███▀▀▀██▄  ███       ▀███████████ ███        ▀▀█████▄        ███ ▀███████████ ███        ▀▀█████▄     ██
██    ███    ██▄ ███         ███    ███ ███    █▄    ███▐██▄       ███   ███    ███ ███    █▄    ███▐██▄    ██
██    ███    ███ ███▌    ▄   ███    ███ ███    ███   ███ ▀███▄     ███   ███    ███ ███    ███   ███ ▀███▄  ██
██  ▄█████████▀  █████▄▄██   ███    █▀  ████████▀    ███   ▀█▀ █▄ ▄███   ███    █▀  ████████▀    ███   ▀█▀  ██ 
██               ▀                                   ▀         ▀▀▀▀▀▀                            ▀          ██
██                                                                                                          ██
██████████████████████████████████████████████████████████████████████████████████████████████████████████████ 
██████████████████████████████████████████████████████████████████████████████████████████████████████████████ 
""")


# --- INITIALIZATION ---
    minimum_bet = 100
    starting_balance = 50 # it is low like this to show functionality. Increase before releasing
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

    # Create players and dealer and sets base wealth to 1000   
    class Clients(Enum): # https://www.geeksforgeeks.org/enum-in-python/
        PLAYER = Player([], 0, None, starting_balance, starting_items)
        CPU1 = Dealer([], 0, "CPU1")
        DEALER = Dealer([], 0, "DEALER")

    game_loop(Clients, minimum_bet)

    ########################################################################################################################################################################
    #######################################################               NOTES               ##############################################################################
    ########################################################################################################################################################################
    # politely ignore this part.
    # I am, in fact, a little bit insane

    # print("\t\t\tDEBUG@main(): flags")
    # for c in (Clients):
    #     c = c.value
    #     print(str(c.get_flags()))

    # for c in (Clients):
    #     c = c.value
    #     print(c)

    # Lose – the player’s bet is taken by the dealer.
    # Win – the player wins as much as they bet. If you bet $10, you win $10 from the dealer (plus you keep your original bet, of course.)
    # Blackjack (natural) – the player wins 1.5 times the bet. With a bet of $10, you keep your $10 and win a further $15 from the dealer.
    # Push – the hand is a draw. The player keeps their bet, neither winning nor losing money.

    # When all players have finished their actions, the dealer turns over their hidden hole card
    # The dealer must hit if the value of the hand is lower than 17, 
        # otherwise the dealer will stand.

#Winning the Game
    # Blackjack: 
        # If your first two cards are an Ace and a 10-value card (10, Jack, Queen, King), this is an automatic win (Blackjack) and pays out at a higher rate than a regular win (usually ×1.5).
    # Higher Value than Dealer: 
        # If your hand total is closer to 21 than the dealer’s hand total without going bust, you win. Winnings are typically paid out at 1:1.
    # Dealer Busts: 
        # If the dealer’s hand total goes over 21 (busts), you win regardless of your hand value.
    # Push: 
        # If your hand total equals the dealer’s hand total, it’s a tie (push) and your bet is returned without any winnings or losses.
    # Lower Value than Dealer: 
        # If the dealer’s hand total is closer to 21 than yours without busting, you lose your bet.
    ########################################################################################################################################################################














def game_loop(clients, min_bet):
    # misc variables
    dealer_nat_black = False
    nat_winners = []
    successful_bet = False

    print("\n\n-+-+- New round start! -+-+-\n\n")

    # user place bet (and sell if can't meet minimum [and lose if broke])
    while not successful_bet:
        bet_outcome = clients.PLAYER.value.bet(min_bet)
        if bet_outcome > 0:
            clients.PLAYER.value.set_player_bet(bet_outcome)
            successful_bet = True
        else:
            sale_outcome = clients.PLAYER.value.sell_item()
            if sale_outcome == -1:
                # no items to sell, game over
                print("HAHAHAHA YOU'RE BROKE GETOUTTAHERE (you lost!)")
                exit()
            else:
                continue

    print("DEBUG@game_loop: player bet:",clients.PLAYER.value.get_player_bet()) #DEBUG

    # Creates a deck and shuffles the deck
    decklist = Deck([])
    decklist.create_deck()
    decklist.shuffle_deck()

    # ensure hands are empty, then draw 2 cards to start
    for x in range(2):
        for c in (clients):
            c = c.value
            c.set_hand([])
            c.draw(decklist.draw_card())
            c.draw(decklist.draw_card())

    check_hands(clients)
    print()
    display_all_hands(clients)

    # determine if end_round conditions are already met (turn-one blackjack)
    for c in (clients):
        if c.value.get_flags()["natural_blackjack"]:
            if c.name == "DEALER":
                print("DEBUG:: !!!DEALER!!!: NAT BLACKJACK")
                dealer_nat_black = True
            else:
                print("DEBUG: "+str(c.name)+": NAT BLACKJACK")
                c.value.set_flag("natural_blackjack", True)
                nat_winners.append(c.name)

    # if a player does have nat blackjack, check the dealer;   if both have nat black, player pushes
    if nat_winners != [] and dealer_nat_black:
        print("DEBUG: dealer+player natural_blackjack; push for player")
        for name in nat_winners:
            clients.name.set_flag("push", True)

    # player wins with nat blackjack
    if len(nat_winners) == 1 and not dealer_nat_black:
        bet_resolution(clients)

    # no nat blackjacks to end game with: continue to 'Hit, Stand, or Bust'
        # TODO 'Hit, Stand, or Bust' (it should probably go in its own function?)
    pass











def bet_resolution(clients):
    # method for resolving bets after a round has ended
    # TODO
    pass

def end_round(clients, decklist):
    # after all players have finished their turn, dealer follows drawing rules
    # TODO
    print("DEBUG@final_turn():") #DEBUG


def check_for_win(clients):
    for c in (clients):
        if c.name == "DEALER" and c.value.get_flags()["bust"]:
            print("*"*20,"DEALER BUST","*"*20)

def display_all_hands(clients, show_hole=False):
    for c in (clients):
        if c.name == "DEALER":
            c.value.set_flag("hide_hole", True)
        print("DEBUG@display_all_hands(): "+c.name,str(c.value.get_flags())) #DEBUG
        print(c.value)

def check_hands(clients):
    # print("\t\tDEBUG@check_hands(): START CHECK")
    for c in clients:
        # print("\nDEBUG@check_hands(): client:"+c.name)
        c = c.value

        if c.get_flags()["bust"]:
            # print("DEBUG@check_hands(): bust is true, skipping...")
            continue

        val = c.get_hand_value()

        if val > 21:
            c.set_flag("bust", True)
        elif val == 21 and len(c.get_hand()) == 2: 
            c.set_flag("natural_blackjack", True)
        elif val == 21: 
            c.set_flag("blackjack", True)

    # DEBUG:: I'm not sure if this will work upon return to the main logic loop
    # for c in clients: #DEBUG
        # c = c.value
        # print("\tDEBUG@check_hands(): printing")
        # print(c.value) #DEBUG
        # print(c.name,str(c.value.get_flags())) #DEBUG


if __name__ == '__main__':
    main()