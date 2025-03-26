### **[ [Click to go Back to Home] ](https://github.com/Purolis/Agile-Group-Project)**
code organization idea content below [(From issue #9)](https://github.com/Purolis/Agile-Group-Project/issues/9)
> # Card class
> 
> We might make cards that _do things_ in the future, so we should have a basic class that defines a card and what attributes it might have.
> 
> Leaves things open and easy to change.
> # Deck class
> 
> Basically a wrapper, contains a dictionary (or similar) populated with cards (instances of Card class).
> 
> making a class for this lets us abstract methods for:
> - deck building (initialization),
> - shuffling, and
> - dealing;
> - If we want to implement "cutting the deck" or something, that would be easy to do with a helper method.
> 
> 
> # Player class
> - hand (what cards are in your possesion?)
> - health? victory points?
> - literally anything else we might add later
