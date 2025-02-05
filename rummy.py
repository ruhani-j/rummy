# welcome message
welcome = "Hello, welcome to Rummy! Hope you have fun!\n"

# instructions
instructions = "Instructions: \n"
instructions += "Rummy is a card game that can be played between two or more people. The object of the game is to 'meld' your cards into two types of combinations. \n"
instructions += "Runs: These are consecutive sequences of three or more cards of the same suit. \n"
instructions += "Sets: These are collections of three or more cards of the same rank (but differing suits) \n"
instructions += "For example, a run can consist of one six of hearts, one seven of spades, and one eight of clubs. Similarly, a set may consist of three sixes of different suits (examples: hearts, spades, and clubs). \n"
instructions += "You can also lay off cards in rummy. Laying off is when a player puts down a card that matches the other player's meld. For example, if player 1 puts down a set of three eights, player 2 can put down another eight to add to the meld. This is another way for a player to get rid of their cards. \n"
instructions += "At the start of the game, the cards are shuffled by the dealer and each player is dealt ten cards. The remaining cards are placed in the center of the table to form the stock. \n"
instructions += "The first card of the stock is placed faced up beside the pile to start off the discard pile (this leaves us with two different piles: the stock and the discard pile). \n"
instructions += "The user will go first, drawing a card from either the stock or the discard pile. Then the player will see if they can create any melded combinations or lay off one (or more) of their cards. \n"
instructions += "If the player cannot make any combinations or lay off a card, then they must discard one of their cards. If the player can meld some of their cards, they will create as many melds as possible and/or lay off a card; after this, the player will discard one of their cards, and it's the next player's turn, following the same rules. \n"
instructions += "The first person to sort their entire hand into the above combinations with a final card to place in the discard pile wins the game. \n"

user_input = input("Type 'instructions' to view the instructions or press Enter to continue: ")

if user_input == "":
    # Display welcome message and instructions if input is empty
    print("")
    print(welcome)
    print(instructions)

elif user_input.lower() == "instructions":
    # Display instructions if the user types 'instructions'
    print(instructions)
