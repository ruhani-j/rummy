"""
@author: Ruhani Jindal and Celeste Lopez Boulton

For the final project, we have decided to create a card game called Rummy.

"""

# ****** Start Game ****** #

# welcome message
welcome = "Hello, welcome to Rummy! Hope you have fun!\n"
welcome += "In the beginning of any turn, you can input instructions, sort by rank, sort by card, or click enter to continue"

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

print(welcome)

# ****** Initializing Cards ****** #

import random

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Define suits and ranks
suits = ['♣', '♥', '♦', '♠']  # Unicode symbols for suits
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

# Create the deck
deck = []

# Generate the deck of 52 cards (Card objects)
for suit in suits:
    for rank in ranks:
        card = Card(suit, rank)
        deck.append(card)

# Make suits and ranks identifiable
hearts = [card for card in deck if card.suit == '♥']
diamonds = [card for card in deck if card.suit == '♦']
spades = [card for card in deck if card.suit == '♠']
clubs = [card for card in deck if card.suit == '♣']

# Create an empty list for the melds
melds = []

computer_score = 0
player_score = 0

# ****** Functions and Descriptions ****** #
# shuffle: shuffles the deck at the beginning of the game
def shuffle(deck):
    random.shuffle(deck)

# deal: deals the computer and player 10 cards each at the beginning of the game
def deal(deck):
    player_hand = [] # create a new list containing the hand of the player

    for i in range(10): # deal 10 cards for each player
        card = deck.pop(0) # remove first element in deck list
        player_hand.append(card) # add the element to the player's hand
    return player_hand


# sort: allows players to sort their hands for ease in viewing
def sort(cards, by = "rank"):

    rank_order = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suit_order = ['♠', '♣', '♥', '♦']

    if by == "rank":
        # Sorting by rank
        cards.sort(key=lambda card: rank_order.index(str(card.rank)))
        print(cards)
    elif by == "suit":
        # Sorting by suit
        cards.sort(key=lambda card: suit_order.index(str(card.suit)))
        print(cards)
    else:
        raise ValueError("Invalid sorting critera. Use 'rank' or 'suit'.")
    return cards

# create_discard_pile: creates discard pile at the beginning of the game
def create_discard_pile():
    discard_pile = []  # create a new list for the discard pile

    card = deck.pop(0) # remove first element in deck list
    discard_pile.append(card)

    return discard_pile

# draw_deck: draws a card from the deck pile
def draw_deck(deck, hand):
    card = deck.pop(0) # remove first element in deck
    hand.append(card) # add element to the hand at play

# draw_discard: draws a card from the discard pile
def draw_discard(discard_pile, hand):
    card = discard_pile.pop(0)  # remove first element in discard pile
    hand.append(card)  # add element to the hand at play

# meld: allows player to create two types of melds: runs and sets
def meld(hand):
    next_move = ""
    while next_move.upper() != 'B':
        print("A - create run")
        print("B - create set")

        choice = input("Enter type of meld: ")

        if choice.upper() == 'A':
            # runs: consecutive values, same rank
            print("Pick 3 or more cards to meld (separate with spaces).")
            print("1st card = 1, 2nd card = 2, ect...")
            print("Your hand: ", hand)
            print("Ex: 1 2 3 (1st, 2nd, and 3rd cards)")

            cards = input("Enter cards: ").split()  # get string of cards

            # convert the list to numbers
            cards = list(map(int, cards))

            # Check to see if the user entered a valid meld
            valid = True
            for i in range(len(cards) - 1):  # loop through chosen meld
                if hand[cards[i + 1] - 1].suit == hand[cards[i] - 1].suit:  # verify the suits are equal
                    if int(hand[cards[i + 1] - 1].rank) == 2 and hand[cards[i] - 1].rank == 'A':
                        valid = True
                    elif int(hand[cards[i + 1] - 1].rank) == int(hand[cards[i] - 1].rank) + 1:  # verify the ranks are consecutive
                        valid = True
                    else:
                        valid = False
                        break
                else:  # if not valid, break out of loop
                    valid = False
                    break
        elif choice.upper() == 'B':
            # sets: same value, different rank
            print("Pick 3 or more cards to meld (separate with spaces).")
            print("1st card = 1, 2nd card = 2, ect...")
            print("Ex: 1 2 3 (1st, 2nd, and 3rd cards)")

            cards = input("Enter cards: ").split() # get string of cards

            # convert the list to numbers
            cards = list(map(int, cards))

            # Check to see if the user entered a valid meld
            valid = True
            for i in range(len(cards) - 1):  # loop through chosen meld
                if hand[cards[i + 1] - 1].rank == hand[cards[i] - 1].rank:  # verify the ranks are equal
                    valid = True
                else: # if not valid, break out of loop
                    valid = False
                    break
        else:
            print("Invalid input")

        # Consequences of valid and invalid melds
        if valid:
          print("VALID MELD")
          for i in range(len(cards)):
              melds.append(hand[cards[i] - 1]) # add meld to meld list
              print("Updated melds: ", melds)
        else:
            print("ERROR: INVALID MELD")
            print("Cannot add meld to existing melds")

        # Choose next steps
        print("What will be your next move?")
        print("A - create another meld")
        print("B - return to other options")

        next_move = input("Enter next move: ")


# layoff: allows player to add to an existing meld
def layoff(melds, hand):
    print("Current melds: ", melds)
    print("Which meld would you like to add to? ")
    print("1st meld = 1, 2nd meld = 2, etc...")
    meld_number = int(input("Enter meld number: "))

    # ensure the selected meld exists
    if meld_number < 1 or meld_number > len(melds) or meld_number.isdigit() == False:
        print("Invalid meld number. Please try again.")
        return

    # select meld
    selected_meld = melds[meld_number - 1]

    print("Selected meld: ", selected_meld)

    # ask player which card to lay off
    print("Cards in your hand: ", hand)
    card_choice = input("Choose a card to lay off (enter the card number): ")
    print("1st card = 1, 2nd card = 2, etc...")
    chosen_card = hand[int(card_choice) - 1]  # Get the selected card from the hand

    # check if it is a valid meld
    valid_layoff = False # set default to false

    # if meld is a set
    if isinstance(selected_meld[0], int):
        if chosen_card.rank == selected_meld[0].rank:
            valid_layoff = True
    else: # run meld
        if chosen_card.rank == selected_meld[0].rank - 1 or chosen_card.rank == selected_meld[-1].rank + 1:
            valid_layoff = True

    if valid_layoff:
        print(f"Valid layoff! Adding {chosen_card} to the meld.")
        selected_meld.append(chosen_card)
        hand.remove(chosen_card)
        print("Updated meld: ", selected_meld)
        print("Updated hand: ", hand)
    else:
        print("Invalid layoff. The card cannot be added to this meld.")

# discard: allows player to discard a card
def discard(discard_pile, hand):
    print("Which card would you like to discard?")
    print(hand)
    print("1st card = 1, 2nd card = 2, etc...")
    card_number = int(input("Enter card number: "))

    discarded_card = hand.pop(card_number - 1) # remove chosen card from hand
    discard_pile.append(discarded_card)  # add discarded card to discard pile

def computer_meld(hand):
    #suits = ['♣', '♥', '♦', '♠']

    # runs: consecutive ranks, same suit
    potential_cards = []

    for i in range(len(suits)):
        current_suit = suits[i] # loop through all four suits
        for j in range(len(hand)):
            if hand[j].suit == current_suit:
                potential_cards.append(hand[j]) # append matching suits to list

        if len(potential_cards) >= 3: # a meld must be 3 or more cards
            print(potential_cards)

            potential_ranks = []

            # find corresponding numerical value of characters
            for x in range(len(potential_cards)):
                if potential_cards[x].rank == 'A':
                    potential_ranks.append(1)
                elif potential_cards[x].rank == '2':
                    potential_ranks.append(2)
                elif potential_cards[x].rank == '3':
                    potential_ranks.append(3)
                elif potential_cards[x].rank == '4':
                    potential_ranks.append(4)
                elif potential_cards[x].rank == '5':
                    potential_ranks.append(5)
                elif potential_cards[x].rank == '6':
                    potential_ranks.append(6)
                elif potential_cards[x].rank == '7':
                    potential_ranks.append(7)
                elif potential_cards[x].rank == '8':
                    potential_ranks.append(8)
                elif potential_cards[x].rank == '9':
                    potential_ranks.append(9)
                elif potential_cards[x].rank == '10':
                    potential_ranks.append(10)
                elif potential_cards[x].rank == 'J':
                    potential_ranks.append(11)
                elif potential_cards[x].rank == 'Q':
                    potential_ranks.append(12)
                elif potential_cards[x].rank == 'K':
                    potential_ranks.append(13)

            print(potential_ranks) # unsorted

            potential_ranks.sort()
            print(potential_ranks) # sorted

            consecutive_indexes = []
            # check to see if there are 3 or more consecutive ranks
            for x in range(len(potential_ranks) - 1):
                if potential_ranks[x] == potential_ranks[x + 1] - 1:
                    consecutive_indexes.append(x)
                    consecutive_indexes.append(x + 1)
                    print("Valid")
                else:
                    print("Invalid")
                    consecutive_indexes = []

            if len(consecutive_indexes) >= 3: # a meld must be three or more cards
                print(consecutive_indexes)

                # remove duplicates
                indexes = []

                for x in consecutive_indexes:
                    if x not in indexes:
                        indexes.append(x)
                print(indexes)

                # add verified cards to meld
                for x in indexes:
                    print(potential_ranks[x])
                # use indexes to access indexes of cards in potential ranks list
                # locate ranks in computer hand

            potential_cards = []

        else:
            potential_cards = [] # empty the list

    # sets: same rank, different suit
    ranks = [] # created empty list to hold rank characters
    for i in range(len(hand)):
        ranks.append(hand[i].rank) # add rank characters to empty list
    print(ranks)

    # Do not compare the last two cards because a meld
    # must be at least 3 cards (hence the 'len(ranks) - 2'
    is_valid_meld = False
    indexes = [] # a list for valid indexes
    for i in range(len(ranks) - 2):
        possible_meld = 1  # start with one card
        possible_index = i # start with current index
        print(f"For: {ranks[i]}\n")
        for j in range(i + 1, len(ranks)):
            if ranks[i] == ranks[j]:
                print("{}. Match")
                possible_meld += 1 # increase possible meld by 1
                indexes.append(j)
            else:
                print("{}. Unmatch")

        if possible_meld >= 3: # a meld must have at least 3 cards
            print("Valid meld")

            # add cards to meld list
            indexes.insert(0, possible_index) # insert first card in 1st index position
            print(indexes)
            for i in indexes:
                melds.append(hand[i]) # add each card from the meld to the meld list
            print("Updated melds: ", melds)
            for i in range(len(indexes)):
                hand.pop(indexes[i] - i) # remove each card from computer hand
            print("Updated hand: ", hand)

        # after you have found a meld, stop looping through list

        else:
            indexes = []

def computer_layoff(computer_hand, melds):
    if not melds:  # check if melds list is empty
        print("No existing melds to lay off on.")
        return False

    rank_order = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    for selected_meld in melds:
        # ensure selected_meld is a list of cards
        if not isinstance(selected_meld, list) or not selected_meld:
            print(f"Error: Expected a list for meld, but got {type(selected_meld)}")
            continue

        for card in computer_hand[:]:  # Iterate over a copy to allow safe removal
            valid_layoff = False

            # Check if the meld is a set (all cards have the same rank)
            if all(c.rank == selected_meld[0].rank for c in selected_meld):
                if card.rank == selected_meld[0].rank:
                    valid_layoff = True

            # Check if the meld is a run (all cards have the same suit and are consecutive)
            elif all(c.suit == selected_meld[0].suit for c in selected_meld):
                card_rank_index = rank_order.index(card.rank)
                first_rank_index = rank_order.index(selected_meld[0].rank)
                last_rank_index = rank_order.index(selected_meld[-1].rank)

                if card_rank_index == first_rank_index - 1 or card_rank_index == last_rank_index + 1:
                    valid_layoff = True

            # If a valid layoff is found, execute it
            if valid_layoff:
                print(f"Computer adds {card} to meld {selected_meld}")
                selected_meld.append(card)

                # Ensure correct order if it's a run
                if all(c.suit == selected_meld[0].suit for c in selected_meld):
                    selected_meld.sort(key=lambda x: rank_order.index(x.rank))

                computer_hand.remove(card)
                print("Updated meld:", selected_meld)
                print("Updated computer hand:", computer_hand)
                return True  # Successfully laid off a card

    print("Computer could not lay off any card.")
    return False


import random
# computer discard: allows the computer to discard a card
def computer_discard(discard_pile, computer_hand):
    if not computer_hand:
        return  # prevents errors if hand is empty

    random_index = random.randint(0, len(computer_hand) - 1)  # choose a random card
    discarded_card = computer_hand.pop(random_index)  # remove chosen card from hand
    discard_pile.append(discarded_card)  # add to discard pile

    print(f"Computer discards {discarded_card}")


def start_turn(player_hand):
    user_input = input("Your turn: ")
    if user_input == "":
        print(player_hand)
        #print()
    elif user_input.lower() == "instructions":
        print(instructions)
    elif user_input.lower() == "sort by rank":
        sort(player_hand, by="rank")
    elif user_input.lower() == "sort by suit":
        sort(player_hand, by="suit")
    elif user_input.lower() == "shuffle" or user_input.lower() == "shuffle deck":
        shuffle(deck)

def computer_turn(computer_hand, melds, discard_pile):
    computer_meld(computer_hand)
    computer_layoff(computer_hand, melds)
    computer_discard(discard_pile, computer_hand)

def play_game():

    # ***** Game Code ***** #
    # shuffle the deck
    shuffle(deck)

    # deal  each player a hand of cards
    computer_hand = deal(deck)
    player_hand = deal(deck)

    # create the discard pile
    discard_pile = create_discard_pile()
    print("Discard Pile: ", discard_pile)

    # print new deck
    print("Deck: ", deck)

    print("Computer hand: ", computer_hand)
    print("Player hand: ", player_hand)

    # Game starts here
    keep_playing = True
    while keep_playing:
        start_turn(player_hand)
        # ****** Drawing a card ****** #
        # choices for picking up a card
        print("A - draw from deck pile")
        print("B - draw from discard pile")

        while True:
            choice = input("Enter choice (A/B): ") # computer or user makes choice
            if choice.upper() in ['A', 'B']:
                break
            print("Invalid input. Please enter 'A' or 'B'.")

        if choice.upper() == 'A':
            draw_deck(deck, player_hand)
        elif choice.upper() == 'B':
            draw_discard(discard_pile, player_hand)
        else:
             print("Invalid input.")

        print("Your hand: ", player_hand)

        # ****** Meld/Layoff and Discard ****** #
        # changed MELD and LAYOFF to separate choices
        while True:
            # placed options inside the loop
            print("A - Meld")
            print("B - Layoff")
            print("C - Discard a card")

            choice = input("Enter choice (A/B/C): ")

            if choice.upper() == 'A':
                meld(player_hand)
            elif choice.upper() == 'B':
                layoff(melds, player_hand)
            elif choice.upper() == 'C':
                discard(discard_pile, player_hand)
                computer_turn(computer_hand, melds, discard_pile)
            else:
                print("Invalid input. Please enter 'A' or 'B' or 'C'.")

        print(discard_pile)

    # ****** Win Detection ****** #
        if len(computer_hand) == 0 or len(player_hand) == 0:
            keep_playing = False

    if len(computer_hand) == 0:
        print("You win! :)")
        computer_score += len(player_hand)
    if len(player_hand) == 0:
        print("You lose :(")
        player_score += len(computer_hand)

    # Print results
    print("Your Score: ", player_score)
    print("Computer Score: ", computer_score)

play_game()

while input("Do you want to play again? (yes/no)") == "yes":
    play_game()
