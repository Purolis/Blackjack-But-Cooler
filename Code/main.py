# NOTE FOR TEAM
# | driver file
# | should be the only file that you run, anything else should be a module
# | separate functions into their own modules as needed

from Card import Card

def main():
    # Right now, this driver just demonstrates functionality of our prototype.
    # in the future, this file will run the game.

    queen_of_spades = Card(1, 12)
    print(queen_of_spades.get_human_value())
    print(queen_of_spades.get_human_suite())
    print()

    king_of_clubs = Card(2, 13)
    print(king_of_clubs.get_human_value())
    print(king_of_clubs.get_human_suite())
    # This is an error!!! it prints 0 of Clubs...
    print()

    jack_of_diamonds = Card(3, 11)
    print(jack_of_diamonds.get_human_value())
    print(jack_of_diamonds.get_human_suite())
    # another error, should be jack, gives ace?
    print()

    ten_of_hearts = Card(4, 10)
    print(ten_of_hearts.get_human_value())
    print(ten_of_hearts.get_human_suite())
    print()

if __name__ == '__main__':
    main()