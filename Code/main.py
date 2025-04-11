from Deck import Deck
from Player import Player
from Dealer import Dealer
from Card import Card
from Colors import Colors
from enum import Enum
import re
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
    starting_balance = 1000
    starting_items = {
        "house": 50_000,
        "firstborn": 30_000,
        "car": 25_000,
        "dog": 666,
        "watch": 500,
        "shoes": 90,
        "pants": 50,
        "shirt": 15,
        "quit": "leave table and exit game"
    }

    # Create players and dealer and sets base wealth to 1000   
    class Clients(Enum): # https://www.geeksforgeeks.org/enum-in-python/
        PLAYER = Player([], 0, None, starting_balance, starting_items)
        CPU1 = Player([], 0, "CPU1", starting_balance, {})
        CPU2 = Player([], 0, "CPU2", starting_balance, {})
        DEALER = Dealer([], 0, "DEALER")

    game_loop(Clients, minimum_bet) # run until player exit or loss
    goodbye()
    exit()

def game_loop(clients, min_bet):
    running = True
    while running:
        print("\n\n-+-+- New round start! -+-+-\n\n")

        # reset statuses
        for c in clients:
            c.value.reset_flags()
            if c.name != 'DEALER':
                c.value.set_player_bet(0)

        # user place bet (and sell if can't meet minimum [and lose if broke])
        did_bet = False
        while not did_bet:
            bet_outcome = clients.PLAYER.value.bet(min_bet)
            if bet_outcome > 0:
                clients.PLAYER.value.set_player_bet(bet_outcome)
                did_bet = True
            else:
                sale_outcome = clients.PLAYER.value.sell_item()
                if sale_outcome == -1:
                    # no items to sell, game over
                    print("You don't have enough money to continue, and have no items to sell!")
                    print("You Lost!")
                    print("Game Over!")
                    running = False
                    did_bet = True
                    return
                elif sale_outcome == -2:
                    # user chose to not sell; quit
                    print("Game Over!")
                    running = False
                    did_bet = True
                    return

        # add CPU bets
        for c in clients:
            if 'cpu' in c.name.lower():
                c.value.set_player_bet(min_bet)
                c.value.set_player_wealth( c.value.get_player_wealth() - c.value.get_player_bet() )
                # print("DEBUG@game_loop: "+c.name+" bet:",c.value.get_player_bet()) #DEBUG

        # Creates a deck and shuffles the deck
        decklist = Deck([])
        decklist.create_deck()
        decklist.shuffle_deck()
        decklist.shuffle_deck()
        decklist.shuffle_deck()

        # ensure hands are empty, then draw 2 cards to start
        for x in range(2):
            for c in (clients):
                c = c.value
                c.set_hand([])
                c.draw(decklist.draw_card())
                c.draw(decklist.draw_card())

        check_hands(clients)
        display_all_hands(clients)

        # check for natural blackjack (first round win)
        nat_bj_winners = []
        for c in (clients):
            if c.value.get_flags()['natural_blackjack']:
                nat_bj_winners.append(c)
        if len(nat_bj_winners) > 0:
            if len(nat_bj_winners) == 1 and nat_bj_winners[0].name == "DEALER":
                # handle edge case where dealer has natural blackjack by themself
                pass
            else:
                # natural blackjack ends round, dealer 
                # cash out for winners, deal new hand
                # print("DEBUG@game_loop: nat_bj_winners: "+str(nat_bj_winners)) #DEBUG
                if clients.DEALER.value.get_flags()['natural_blackjack']:
                    # if dealer also has nat bj, players push
                    for c in nat_bj_winners:
                        c.value.set_flag('push', True)
                cpu_resolve(clients, decklist)
                outcome_txt = victory_resolution(clients)
                print()
                print(outcome_txt)
        else:
            # no nat blackjacks to end game with: player continues to 'Hit, Stand, or Bust'
            c_flag = clients.PLAYER.value.get_flags()
            while not c_flag["bust"] and not c_flag["finished_turn"]:
                c_decision = hit_stand(clients.PLAYER)
                if c_decision == 'hit':
                    clients.PLAYER.value.draw(decklist.draw_card())
                    check_hands(clients)
                    print(clients.PLAYER.value)
                else:
                    clients.PLAYER.value.set_flag('finished_turn', True)
                # update flags for next iteration
                check_hands(clients)
                c_flag = clients.PLAYER.value.get_flags()

            # after player is done, let CPU and Dealer play
            cpu_resolve(clients, decklist)

            # end-of-round display, dealer flips hole card
            check_hands(clients)
            outcome_txt = victory_resolution(clients)
            display_all_hands(clients, hide_hole=False)
            print()
            print(outcome_txt)

def victory_resolution(clients):
    # print("DEBUG@victory_resolution()") #DEBUG
    check_hands(clients)
    outcome_txt = ""

    for c in clients:
        if c.name == 'DEALER':
            pass
        elif c.value.get_flags()['natural_blackjack']: 
        # win: natural blackjack, insta-win for player, winnings = 1.5 × bet
            if clients.DEALER.value.get_flags()['natural_blackjack']:
            # push: dealer ties player's natural blackjack
                bet = c.value.get_player_bet()
                wealth = c.value.get_player_wealth()
                c.value.set_player_wealth(wealth + bet)
                c.value.set_flag('push', True)
                outcome_txt += c.name+" tied with dealer!\n"
            bet = c.value.get_player_bet()
            wealth = c.value.get_player_wealth()
            winnings = int(bet*2.5)
            c.value.set_player_wealth(wealth + winnings)
            outcome_txt += c.name+" has natural blackjack! They won $"+str(winnings)+"\n"
        elif clients.DEALER.value.get_flags()['bust']:
        # win: dealer bust, everyone wins regardless of hand
            if re.search("^PLAYER|^CPU", c.name): # RegEx for name search
                # print("DEBUG@victory_resolution(): "+c.name+" check") #DEBUG
                bet = c.value.get_player_bet()
                wealth = c.value.get_player_wealth()
                winnings = bet*2
                c.value.set_player_wealth(wealth + winnings)
                outcome_txt += "Dealer bust! "+c.name+" won $"+str(winnings)+"\n"
        elif c.value.get_flags()["bust"]:
        # lose: player bust, lose bet
            outcome_txt += c.name+" busted and lost their bet of $"+str(c.value.get_player_bet())+"\n"
        elif c.value.get_hand_value() == clients.DEALER.value.get_hand_value():
        # tie: push, return bet to player
            bet = c.value.get_player_bet()
            wealth = c.value.get_player_wealth()
            c.value.set_player_wealth(wealth + bet)
            c.value.set_flag('push', True)
            outcome_txt += c.name+" tied with dealer!\n"
        elif c.value.get_flags()['blackjack']:
        # win: regular blackjack, winnings = 1.5 × bet
            bet = c.value.get_player_bet()
            wealth = c.value.get_player_wealth()
            winnings = int(bet*2.5)
            c.value.set_player_wealth(wealth + winnings)
            outcome_txt += c.name+" has blackjack! They won $"+str(winnings)+"\n"
        elif c.value.get_hand_value() > clients.DEALER.value.get_hand_value():
        # win: higher value than dealer
            bet = c.value.get_player_bet()
            wealth = c.value.get_player_wealth()
            winnings = bet*2
            c.value.set_player_wealth(int(wealth + winnings))
            outcome_txt += c.name+" beat the dealer! They won $"+str(winnings)+"\n"
        elif c.value.get_hand_value() < clients.DEALER.value.get_hand_value():
        # lose: lower value than dealer
            outcome_txt += c.name+" lost to the dealer!\n"
        else:
            print("AAAAAAAAHHHHHH!!! There was an error! This shouldn't happen!")

    return outcome_txt

def cpu_resolve(clients, decklist):
    # rules for CPU and Dealer drawing (CPU follow same rules as dealer)
        # Dealer Hits: The dealer is required to draw if they have a hand of less than 17. 
        # Dealer Stands: The dealer is required to stand with 17 and more in their hand. 
    check_hands(clients)
    for c in (clients):
        if "PLAYER" not in c.name:
            # print("DEBUG@cpu_resolve(): CPU play!",c.name)
            if c.value.get_flags()['natural_blackjack']:
                pass
            else:
                while c.value.get_hand_value() < 17:
                    c.value.draw(decklist.draw_card())
            c.value.set_flag('finished_turn', True)

def hit_stand(c):
    # gets user decision for hitting or standing
    valid_choice = False
    while not valid_choice:
        try:
            choice = str(input( (str(c.name)+" > Hit or stand? :") ))
            if choice.lower() in ('h','hit'):
                print(str(c.name) + " hits...")
                choice = 'hit'
                valid_choice = True
            elif choice.lower() in ('s', 'stand'):
                print(str(c.name) + " stands...")
                choice = 'stand'
                valid_choice = True
            else:
                print(Colors.red+"Please enter a valid input ('h','hit','s','stand')"+Colors.reset)
        except KeyboardInterrupt:
            print(Colors.red+"\nquitting..."+Colors.reset)
            goodbye()
            exit()
        except BaseException as e:
            # print(e) #DEBUG
            print(Colors.red+"Ya broke it! Try again."+Colors.reset)

    if choice == 'hit':
        return "hit"
    else:            
        return "stand"

def display_all_hands(clients, hide_hole=True):
    time.sleep(0.5)
    print()
    print("┇"*50)
    print()
    for c in (clients):
        if re.search("DEALER|PLAYER", c.name):
            continue
        # print("DEBUG@display_all_hands(): "+c.name,str(c.value.get_flags())) #DEBUG
        print(c.value)
        time.sleep(0.1)

    
    clients.DEALER.value.set_flag("hide_hole", hide_hole)
    print(clients.DEALER.value)
    time.sleep(0.1)
    print(clients.PLAYER.value)


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

def goodbye():

    print("""
  _   _                 _             
 | | | |               | |            
 | |_| |__   __ _ _ __ | | _____      
 | __| '_ \\ / _` | '_ \\| |/ / __|     
 | |_| | | | (_| | | | |   <\\__ \\     
  \\__|_| |_|\\__,_|_| |_|_|\\_\\___/     
  / _|                                
 | |_ ___  _ __                       
 |  _/ _ \\| '__|                      
 | || (_) | |                         
 |_| \\___/|_|         _             _ 
       | |           (_)           | |
  _ __ | | __ _ _   _ _ _ __   __ _| |
 | '_ \\| |/ _` | | | | | '_ \\ / _` | |
 | |_) | | (_| | |_| | | | | | (_| |_|
 | .__/|_|\\__,_|\\__, |_|_| |_|\\__, (_)
 | |             __/ |         __/ |  
 |_|            |___/         |___/   
 """)


if __name__ == '__main__':
    main()