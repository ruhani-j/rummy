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

def shuffle(deck):
    random.shuffle(deck)

def deal(deck):
    player_hand = [] # create a new list containing the hand of the player

    for i in range(10): # deal 10 cards for each player
        card = deck.pop(0) # remove first element in deck list
        player_hand.append(card) # add the element to the player's hand
    return player_hand

shuffle(deck) # shuffle the deck

# deal each player a hand of cards
computer_hand = deal(deck)
player_hand = deal(deck)

print(computer_hand)
print(player_hand)
