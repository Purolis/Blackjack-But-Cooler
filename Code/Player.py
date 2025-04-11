from Dealer import Dealer
from Colors import Colors


class Player(Dealer):
    # Default Variables
    __player_wealth = 0
    __player_bet = 0
    __items = {}

    # Initialization
    def __init__(self, hand, hand_value, name, wealth, items):
        super().__init__(hand, hand_value, name)
        self.set_player_wealth(wealth)
        self.set_items(items)

    # helpers
    def sell_item(self):
        """
        returns 0 for successful item sell; -1 for "unable to sell"
        """
        # check for empty inventory
        if len(self.get_items()) <= 1:
            return -1 # error code, no items to sell, tell game to quit
        else:
            # display options to player
            print("Choose which item to sell 🡻 (type the full word of the item)")
            item_list = ""
            for i in self.get_items():
                if i == "quit":
                    item_list += "├─ " + str(i.title()) + " : " + str(self.get_value(i)) + "\n"
                else:
                    item_list += "├─ " + str(i.title()) + " : $" + str(self.get_value(i)) + "\n"
            print(item_list)

            # input validation for player selection
            valid = False
            choice = None
            while not valid:
                try:
                    choice = str(input(": ")).lower()
                except TypeError:
                    print(Colors.red+"Invalid selection (not a string), please choose an item on the list above."+Colors.reset)
                    continue
                except KeyboardInterrupt:
                    print(Colors.red+"\nquitting..."+Colors.reset)
                    exit()
                except BaseException:
                    print(Colors.red+"I'm not sure what you did, but you broke it, congrats."+Colors.reset)
                    print(Colors.red+"Invalid selection, please choose an item on the list above."+Colors.reset)
                    continue
                else:
                    if choice in self.get_items():
                        valid = True
                    else:
                        print(Colors.red+"Invalid selection, please choose an item on the list above."+Colors.reset)

            if choice == "dog":  # shame the user for selling the dog
                print(Colors.red + """
▓██   ██▓ ▒█████   █    ██                                       
 ▒██  ██▒▒██▒  ██▒ ██  ▓██▒                                      
  ▒██ ██░▒██░  ██▒▓██  ▒██░                                      
  ░ ▐██▓░▒██   ██░▓▓█  ░██░                                      
  ░ ██▒▓░░ ████▓▒░▒▒█████▓                                       
   ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒                                       
 ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░                                       
 ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░                                       
 ░ ░         ░ ░     ░                                           
 ░ ░                                                             
 ███▄ ▄███▓ ▒█████   ███▄    █   ██████ ▄▄▄█████▓▓█████  ██▀███  
▓██▒▀█▀ ██▒▒██▒  ██▒ ██ ▀█   █ ▒██    ▒ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
▓██    ▓██░▒██░  ██▒▓██  ▀█ ██▒░ ▓██▄   ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
▒██    ▒██ ▒██   ██░▓██▒  ▐▌██▒  ▒   ██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
▒██▒   ░██▒░ ████▓▒░▒██░   ▓██░▒██████▒▒  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░  ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
░  ░      ░  ░ ▒ ▒░ ░ ░░   ░ ▒░░ ░▒  ░ ░    ░     ░ ░  ░  ░▒ ░ ▒░
░      ░   ░ ░ ░ ▒     ░   ░ ░ ░  ░  ░    ░         ░     ░░   ░ 
       ░       ░ ░           ░       ░              ░  ░   ░                                         
You sold your dog, I hope you're happy, malignant oaf."""+Colors.reset)

            if choice == "quit":
                print("You leave the table with your dignity.")
                return -2 # player quit
            # update player wealth and items
            new_items = self.get_items()
            gained_wealth = new_items[choice]
            print("Gained wealth: $" + str(gained_wealth))

            self.set_player_wealth(self.get_player_wealth() + gained_wealth)

            del (new_items[choice])
            self.set_items(new_items)
            print("New wealth total: $" + str(self.get_player_wealth()))
            return 0  # ran without issue

    def bet(self, minimum=100, amount=None):
        # minimum bet: $100
        # make sure user can't bet more than they have, or negative values
        # if user is out of money, call sell_item(); maybe put that into main with a check
        # print("DEBUG@Player.py@bet()")

        if self.get_player_wealth() < minimum:
            print(Colors.red + "You don't have enough money to make the minimum bet!" + Colors.reset)
            print("You must sell an item to continue playing.")
            return -1  # user is poor, sell items then retry
        if amount == None:
            valid = False
            while not valid:
                print("\nYou have $" + str(self.get_player_wealth()))
                print("Minimum bet: $" + str(minimum))
                try:
                    choice = int(input("How much would you like to bet? : $"))
                except (TypeError, ValueError):
                    print(Colors.red + "Please enter an integer dollar ammount." + Colors.reset)
                except KeyboardInterrupt:
                    print(Colors.red+"\nquitting..."+Colors.reset)
                    exit()
                except BaseException as e:
                    print(Colors.red + "Not sure what you did, but you broke it!" + Colors.reset)
                else:
                    if choice > self.get_player_wealth():
                        print(Colors.red+"That's more money than you have!"+Colors.reset)
                    elif choice <= 0:
                        print(Colors.red+"Bet amount must be positive."+Colors.reset)
                    elif choice < minimum:
                        print(Colors.red + "You must at least bet the minimum bet. ($" + str(
                            minimum) + ")" + Colors.reset)
                    else:
                        valid = True
    # Getters
    def get_player_wealth(self):
        return self.__player_wealth

    def get_items(self):
        return self.__items

    def get_value(self, item):
        return self.__items.get(item)

    def get_all_items(self):
        return len(self.__items)

    def get_player_bet(self):
        return self.__player_bet

    # Setters
    def set_player_wealth(self, player_wealth):
        self.__player_wealth = player_wealth

    def set_items(self, items):
        self.__items = items

    def set_player_bet(self, bet):
        self.__player_bet = bet

    # to_string
    def __str__(self):
        txt = ""
        txt += super().__str__()
        txt = txt[:-29] # get rid of end-cap to append information
        txt += "\n"
        if self.get_name() is None:
            txt += "├─ Your Wealth: $" + str(self.get_player_wealth()) + "\n"
            txt += "├─ Your Bet: $" + str(self.get_player_bet()) + "\n"
        else:
            txt += "├─ " + str(super().get_name()) + " wealth: $" + str(self.get_player_wealth()) + "\n"
            txt += "├─ " + str(super().get_name()) + " bet: $" + str(self.get_player_bet()) + "\n"
        txt += "╘═══════════════════════"+Colors.reset

        return txt
