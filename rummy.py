import random

deck = ['A of ♣', # clubs
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

        'A of ♥', # hearts
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

        'A of ♦', # diamonds
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
        ] # end of deck

def shuffle(deck):
    random.shuffle(deck)

print(shuffle(deck))


