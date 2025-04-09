from Dealer import Dealer


class Player(Dealer):

    # Default Variables
    __player_wealth = 0
    __items = {}

    # Initialization
    def __init__(self, hand, hand_value, name, wealth, items):
        super().__init__(hand, hand_value, name)
        self.set_player_wealth(wealth)
        self.set_items(items)

    # helpers

    # def count_hand(self):
    #     super().count_hand()


    def sell_item(self):
        """
        returns 0 for successful item sell; -1 for "unable to sell"
        """
        # check for empty inventory
        if self.get_items() == {}:
            print("You have no items to sell!")
            return -1 # error code, no items to sell, tell game to quit
        else:
            # display options to player
            print("Choose which item to sell 🡻 (type the full word of the item)")
            item_list = ""
            for i in self.get_items():
                item_list += "├─ " + str(i.title()) + " : $" + str(self.get_value(i)) + "\n"
            print(item_list)

            # input validation for player selection
            valid = False
            choice = None
            while not valid:
                try:
                    choice = str(input(": ")).lower()
                except TypeError:
                    print("Invalid selection (not a string), please choose an item on the list above.")
                    continue
                except BaseException:
                    print("I'm not sure what you did, but you broke it, congrats.")
                    print("Invalid selection, please choose an item on the list above.")
                    continue
                else:
                    if choice in self.get_items():
                        valid = True
                    else:
                        print("Invalid selection, please choose an item on the list above.")

            if choice == "dog": # shame the user for selling the dog
                print("""\033[38;5;9m
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
                \033[0m""")

            # update player wealth and items
            new_items = self.get_items()
            gained_wealth = new_items[choice]
            print("Gained wealth: $"+str(gained_wealth))

            self.set_player_wealth(self.get_player_wealth()+gained_wealth)

            del(new_items[choice])
            self.set_items(new_items)
            print("New wealth total: $"+str(self.get_player_wealth()))
            return 0 # ran without issue

    def bet(minimum=0):
        # minimum bet: $100
        # make sure user can't bet more than they have, or negative values
        # if user is out of money, call sell_item(); maybe put that into main with a check
        pass

    def print_item(self, item):
        print(f'You sold your {item}! You got ${self.get_value(item)} for it!')
        self.set_player_wealth(self.__items.pop(item))

    # Getters
    def get_player_wealth(self):
        return self.__player_wealth

    def get_items(self):
        return self.__items

    def get_value(self, item):
        return self.__items.get(item)

    def get_all_items(self):
        return len(self.__items)

    # Setters
    def set_player_wealth(self, player_wealth):
        self.__player_wealth = player_wealth

    def set_items(self, items):
        self.__items = items

    # to_string
    def __str__(self):
        txt = ""
        txt += super().__str__()
        txt = txt[:-31] # get rid of end-cap to append information
        txt += "\n"
        if self.get_name() is None:
            txt += "├─ Your Wealth: $" + str(self.get_player_wealth()) + "\n"
        else:
            txt += "├─ " + str(super().get_name()) + " wealth: $" + str(self.get_player_wealth()) + "\n"
        txt += "└───────────────────────\033[0m\n\n"
            # \033[0m 🡺 reset text color

        return txt