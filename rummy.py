import random

deck = ['A of ♣',  # club
        '2 of ♣',
        '3 of ♣',
        '4 of ♣',
        '5 of ♣',
        '6 of ♣',
        '7 of ♣',
        '8 of ♣',
        '9 of ♣',
        '10 of ♣',
        'J of ♣',
        'Q of ♣',
        'K of ♣',

        'A of ♥',  # hearts
        '2 of ♥',
        '3 of ♥',
        '4 of ♥',
        '5 of ♥',
        '6 of ♥',
        '7 of ♥',
        '8 of ♥',
        '9 of ♥',
        '10 of ♥',
        'J of ♥',
        'Q of ♥',
        'K of ♥',

        'A of ♦',  # diamonds
        '2 of ♦',
        '3 of ♦',
        '4 of ♦',
        '5 of ♦',
        '6 of ♦',
        '7 of ♦',
        '8 of ♦',
        '9 of ♦',
        '10 of ♦',
        'J of ♦',
        'Q of ♦',
        'K of ♦',

        'A of ♠', # spades
        '2 of ♠',
        '3 of ♠',
        '4 of ♠',
        '5 of ♠',
        '6 of ♠',
        '7 of ♠',
        '8 of ♠',
        '9 of ♠',
        '10 of ♠',
        'J of ♠',
        'Q of ♠',
        'K of ♠',
        ] # end of deck list

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

# discard: allows player to discard a card
def discard(discard_pile, hand):
    print("Which card would you like to discard?")
    print("1st card = 1, 2nd card = 2, ect...")
    card_number = int(input("Enter card number: "))

    discarded_card = hand.pop(card_number - 1) # remove chosen card from hand
    discard_pile.append(discarded_card)  # add discarded card to discard pile

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
    # ****** Drawing a card ****** #
    # choices for picking up a card
    print("A - draw from deck pile")
    print("B - draw from discard pile")

    choice = input("Enter choice: ") # user makes choice

    if choice.upper() == 'A':
        draw_deck(deck, player_hand)
    elif choice.upper() == 'B':
        draw_discard(discard_pile, player_hand)
    else:
        print("Invalid input.")

    print("Your hand: ", player_hand)

    # ****** Meld/Layoff and Discard ****** #
    print("A - Meld/Layoff")
    print("B - Discard a card")

    choice = input("Enter choice: ")  # computer or user makes choice

    if choice.upper() == 'A':
        print("A")
    elif choice.upper() == 'B':
        discard(discard_pile, player_hand)
        print("Your hand: ", player_hand)
    else:
        print("Invalid Input")

    if len(computer_hand) == 0 or len(player_hand) == 0:
        keep_playing = False
