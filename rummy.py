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
instructions += "Rummy is a card game that can be played between two or more people. \nThe object of the game is to 'meld' your cards into two types of combinations. \n"
instructions += "Runs: These are consecutive sequences of three or more cards of the same suit. \n"
instructions += "Sets: These are collections of three or more cards of the same rank (but differing suits) \n"
instructions += "For example, a run can consist of one six of hearts, one seven of spades, and one eight of clubs. \nSimilarly, a set may consist of three sixes of different suits (examples: hearts, spades, and clubs). \n"
instructions += "You can also lay off cards in rummy. Laying off is when a player puts down a card that matches the other player's meld. \nFor example, if player 1 puts down a set of three eights, player 2 can put down another eight to add to the meld. \nThis is another way for a player to get rid of their cards. \n"
instructions += "At the start of the game, the cards are shuffled by the dealer and each player is dealt ten cards. \nThe remaining cards are placed in the center of the table to form the stock. \n"
instructions += "The first card of the stock is placed faced up beside the pile to start off the discard pile \n(this leaves us with two different piles: the stock and the discard pile). \n"
instructions += "The user will go first, drawing a card from either the stock or the discard pile. \nThen the player will see if they can create any melded combinations or lay off one (or more) of their cards. \n"
instructions += "If the player cannot make any combinations or lay off a card, then they must discard one of their cards. \nIf the player can meld some of their cards, they will create as many melds as possible and/or lay off a card; \nafter this, the player will discard one of their cards, and it's the next player's turn, following the same rules. \n"
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

    CARDS_PER_HAND = 10

    for i in range(CARDS_PER_HAND): # deal 10 cards for each player
        card = deck.pop() # remove first element in deck list
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

# helper function
def rank_to_value(rank):

    mapping = {
        'A': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 11,
        'Q': 12,
        'K': 13
    }
    return mapping.get(rank, 0)

# create_discard_pile: creates discard pile at the beginning of the game
def create_discard_pile():
    discard_pile = []  # create a new list for the discard pile

    card = deck.pop() # remove first element in deck list
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
def meld(hand, melds):
    next_move = ""
    while next_move.upper() != 'B':
        print("A - create run")
        print("B - create set")

        choice = input("Enter type of meld: ")

        # default is false
        valid = False

        if choice.upper() == 'A':
            # runs: consecutive values, same suit
            print("Pick 3 or more cards to meld (separate with spaces).")
            print("1st card = 1, 2nd card = 2, etc...")
            print("Ex: 1 2 3 (1st, 2nd, and 3rd cards)")
            print("Your hand: ", hand)

            cards = input("Enter cards: ").split()  # get string of cards

            # convert the list to numbers
            cards = list(map(int, cards))

            # Check if all indices are valid
            if any(card > len(hand) or card < 1 for card in cards):
                print("ERROR: Invalid card index. Please select valid cards from your hand.")
                continue

            # Check to see if the user entered a valid meld
            valid = True
            for i in range(len(cards) - 1):  # loop through chosen meld
                current_card = hand[cards[i] - 1]
                next_card = hand[cards[i + 1] - 1]

                if current_card.suit == next_card.suit:  # verify the suits are equal
                    # Handle Ace as both high and low
                    if (current_card.rank == 'A' and next_card.rank == 'K') or \
                       (current_card.rank == 'K' and next_card.rank == 'A'):
                        continue  # Ace-King case, loop around
                    elif (int(next_card.rank) == int(current_card.rank) + 1):  # check for consecutive ranks
                        continue  # valid sequence
                    else:
                        valid = False
                        break
                else:  # if suits do not match
                    valid = False
                    break

        elif choice.upper() == 'B':
            # sets: same value, different suits
            print("Pick 3 or more cards to meld (separate with spaces).")
            print("1st card = 1, 2nd card = 2, etc...")
            print("Ex: 1 2 3 (1st, 2nd, and 3rd cards)")

            cards = input("Enter cards: ").split()  # get string of cards

            # convert the list to numbers
            cards = list(map(int, cards))

            # Check if all indices are valid
            if any(card > len(hand) or card < 1 for card in cards):
                print("ERROR: Invalid card index. Please select valid cards from your hand.")
                continue

            # Check to see if the user entered a valid meld
            valid = True
            for i in range(len(cards) - 1):  # loop through chosen meld
                if hand[cards[i + 1] - 1].rank == hand[cards[i] - 1].rank:  # verify the ranks are equal
                    valid = True
                else:  # if not valid, break out of loop
                    valid = False
                    break
        else:
            print("Invalid input")

        # Consequences of valid and invalid melds
        if valid:
            print("VALID MELD")
            # Adjust the cards list to ensure we're removing from the correct indices
            # Remove the cards in reverse order to avoid affecting the indices
            for i in sorted(cards, reverse=True):
                card_to_add = hand[i - 1]
                melds.append(card_to_add)  # add meld to meld list
                hand.remove(card_to_add)  # remove the card from the hand
            print("Updated melds: ", melds)
            print("Updated hand: ", hand)
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

    if len(melds) == 0:
        print("There are no existing melds to lay off on. Please try again")
        return

    print("Current melds: ", melds)
    print("Which meld would you like to add to? ")
    print("1st meld = 1, 2nd meld = 2, etc...")
    while True:
        try:
            meld_number = int(input("Enter meld number: "))
            break  # Exit the loop if input is valid
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

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
    while True:
        try:
            card_number = int(input("Enter card number: "))
            if 1 <= card_number <= len(hand):
                break  # Valid index, exit loop.
            else:
                print(f"Please enter a number between 1 and {len(hand)}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    discarded_card = hand.pop(card_number - 1) # remove chosen card from hand
    discard_pile.append(discarded_card)  # add discarded card to discard pile

def computer_meld(hand):
    meld_created = False
    # ****** runs: consecutive ranks, same suit ******
    potential_cards = []

    for i in range(len(suits)): # the suits are the following: ['♣', '♥', '♦', '♠']
        current_suit = suits[i] # loop through all four suits
        for j in range(len(hand)):
            if hand[j].suit == current_suit:
                potential_cards.append(hand[j]) # append matching suits to list

        if len(potential_cards) >= 3: # a meld must be 3 or more cards

            unsorted_potential_ranks = []

            # find corresponding numerical value of characters
            for x in range(len(potential_cards)):
                unsorted_potential_ranks.append(rank_to_value(potential_cards[x].rank))

            # created a sorted version of the potential ranks
            sorted_potential_ranks = unsorted_potential_ranks.copy()
            sorted_potential_ranks.sort()

            consecutive_indexes = []
            # check to see if there are 3 or more consecutive ranks
            for x in range(len(sorted_potential_ranks) - 1):
                if sorted_potential_ranks[x] == sorted_potential_ranks[x + 1] - 1:
                    consecutive_indexes.append(x)
                    consecutive_indexes.append(x + 1)
                    if len(consecutive_indexes) >= 3:
                        is_valid_meld = True
                else:
                    consecutive_indexes = []
                    is_valid_meld = False

            if is_valid_meld: # a meld must be three or more cards
                # remove duplicates
                indexes = []
                for x in consecutive_indexes:
                    if x not in indexes:
                        indexes.append(x)

                # add the meld to the melds list and remove the cards from the computer's hand
                new_meld = []
                for x in indexes:
                    for y in range(len(unsorted_potential_ranks)):
                        if unsorted_potential_ranks[y] == sorted_potential_ranks[x]:
                            new_meld.append(potential_cards[y])
                            hand.remove(potential_cards[y])
                            break

                melds.append(new_meld)  # add the complete meld as one group

                print("The computer created a new meld")
                print("Updated melds: ", melds)
                #print("Updated computer hand, ", hand)
                meld_created = True

            potential_cards = [] # empty the potential cards list# if the

        else: # if there aren't more than 3 cards, a meld is not possible
            potential_cards = [] # empty the list

    # ****** sets: same rank, different suit ******
    ranks = [] # created empty list to hold rank characters
    for i in range(len(hand)):
        ranks.append(hand[i].rank) # add rank characters to empty list

    # Do not compare the last two cards because a meld
    # must be at least 3 cards (hence the 'len(ranks) - 2'
    is_valid_meld = False
    indexes = [] # a list for valid indexes
    for i in range(len(ranks) - 2):
        possible_meld = 1  # start with one card
        possible_index = i # start with current index
        for j in range(i + 1, len(ranks)):
            if ranks[i] == ranks[j]:
                possible_meld += 1 # increase possible meld by 1
                indexes.append(j)

        if possible_meld >= 3: # a meld must have at least 3 cards
            indexes.insert(0, possible_index) # insert first card in 1st index position
            # **FIX**: Instead of creating separate melds for each card, create one meld from all indexes
            set_meld = [hand[i] for i in indexes]
            melds.append(set_meld)
            print("The computer created a new meld")
            print("Updated melds: ", melds)
            for i in range(len(indexes)):
                hand.pop(indexes[i] - i) # remove each card from computer hand
            #print("Updated computer hand: ", hand)
            meld_created = True

        else:
            indexes = []

    if not meld_created:
        print("The computer does not want to create a new meld")

def computer_layoff(computer_hand, melds):
    if not melds:  # check if melds list is empty
        print("No existing melds for computer to lay off on.")
        return

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
                # Extract ranks of the selected meld and sort them
                selected_ranks = [card.rank for card in selected_meld]
                selected_ranks.sort(key=lambda rank: rank_order.index(rank))  # Sort by rank order

                # Get first and last ranks in the sorted list
                first_rank = selected_ranks[0]
                last_rank = selected_ranks[-1]

                # Now check if the card fits before the first or after the last card
                if card.suit == selected_meld[0].suit:  # Check if card suit matches
                    if rank_order.index(card.rank) == rank_order.index(first_rank) - 1 or rank_order.index(card.rank) == rank_order.index(last_rank) + 1:
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
                #print("Updated computer hand:", computer_hand)
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
    #print("Deck: ", deck)

    #print("Computer hand: ", computer_hand)
    print("Player hand: ", player_hand)

    # Game starts here
    keep_playing = True
    while keep_playing:
        start_turn(player_hand)
        # ****** Drawing a card ****** #
        # choices for picking up a card
        #print("Discard Pile: ", discard_pile[0])
        print("A - Draw from deck pile")
        print(f"B - Draw from discard pile (Pick up the {discard_pile[-1]})")

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
                meld(player_hand, melds)
            elif choice.upper() == 'B':
                layoff(melds, player_hand)
            elif choice.upper() == 'C':
                discard(discard_pile, player_hand)
                computer_turn(computer_hand, melds, discard_pile)
                break
            else:
                print("Invalid input. Please enter 'A' or 'B' or 'C'.")

        #print(discard_pile)

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
