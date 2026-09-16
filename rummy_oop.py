import random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other):
        return isinstance(other, Card) and self.suit == other.suit and self.rank == other.rank


class Deck:
    suits = ["♣", "♥", "♦", "♠"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            raise IndexError("No cards left in the deck.")
        return self.cards.pop(0)

    def deal(self, count):
        hand = []
        for _ in range(count):
            hand.append(self.draw())
        return hand


class Hand:
    def __init__(self, cards=None):
        self.cards = cards[:] if cards else []

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __repr__(self):
        return str(self.cards)

    def add(self, card):
        self.cards.append(card)

    def remove_by_index(self, index):
        if index < 0 or index >= len(self.cards):
            raise IndexError("Card index out of range")
        return self.cards.pop(index)

    def remove_card(self, card):
        self.cards.remove(card)

    def sort(self, by="rank"):
        rank_order = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suit_order = ["♠", "♣", "♥", "♦"]

        if by == "rank":
            self.cards.sort(key=lambda card: rank_order.index(str(card.rank)))
        elif by == "suit":
            self.cards.sort(key=lambda card: suit_order.index(str(card.suit)))
        else:
            raise ValueError("Invalid sorting criteria. Use 'rank' or 'suit'.")
        return self.cards


class Meld:
    def __init__(self, cards):
        self.cards = cards

    def __repr__(self):
        return str(self.cards)

    @property
    def kind(self):
        if self.is_run():
            return "run"
        if self.is_set():
            return "set"
        return "invalid"

    def is_run(self):
        if len(self.cards) < 3:
            return False
        suits = {card.suit for card in self.cards}
        if len(suits) != 1:
            return False
        values = sorted([rank_to_value(card.rank) for card in self.cards])
        for i in range(1, len(values)):
            if values[i] != values[i - 1] + 1:
                return False
        return True

    def is_set(self):
        if len(self.cards) < 3:
            return False
        ranks = {card.rank for card in self.cards}
        if len(ranks) != 1:
            return False
        suits = {card.suit for card in self.cards}
        return len(suits) == len(self.cards)

    def can_add_card(self, card):
        if self.is_run():
            if card.suit != self.cards[0].suit:
                return False
            values = sorted({rank_to_value(c.rank) for c in self.cards} | {rank_to_value(card.rank)})
            return values == list(range(min(values), max(values) + 1))
        if self.is_set():
            return card.rank == self.cards[0].rank and card.suit not in {c.suit for c in self.cards}
        return False

    def add_card(self, card):
        if not self.can_add_card(card):
            raise ValueError("Card cannot be added to this meld")
        self.cards.append(card)


class RummyGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand(self.deck.deal(10))
        self.computer_hand = Hand(self.deck.deal(10))
        self.discard_pile = [self.deck.draw()]
        self.melds = []
        self.turn = "player"

    def rank_to_value(self, rank):
        return rank_to_value(rank)

    def draw_from_stock(self, hand):
        hand.add(self.deck.draw())

    def draw_from_discard(self, hand):
        if not self.discard_pile:
            raise IndexError("Discard pile is empty")
        hand.add(self.discard_pile.pop())

    def create_meld(self, hand, indices, meld_type):
        if len(indices) < 3:
            raise ValueError("A meld must contain at least 3 cards.")

        selected = [hand.cards[i] for i in indices]
        meld = Meld(selected)

        if meld_type == "run" and not meld.is_run():
            raise ValueError("Selected cards do not form a valid run.")
        if meld_type == "set" and not meld.is_set():
            raise ValueError("Selected cards do not form a valid set.")

        for index in sorted(indices, reverse=True):
            hand.remove_by_index(index)

        self.melds.append(meld)
        return meld

    def layoff(self, hand, meld, card_index):
        card = hand.cards[card_index]
        meld.add_card(card)
        hand.remove_card(card)

    def discard_card(self, hand, index):
        card = hand.remove_by_index(index)
        self.discard_pile.append(card)
        return card

    def computer_turn(self):
        top_card = self.discard_pile[-1]
        if self._is_useful(top_card, self.computer_hand.cards):
            self.draw_from_discard(self.computer_hand)
        else:
            self.draw_from_stock(self.computer_hand)

        self._computer_meld()

        if self.computer_hand.cards:
            card_to_discard = self.computer_hand.cards[0]
            self.computer_hand.remove_card(card_to_discard)
            self.discard_pile.append(card_to_discard)

    def _is_useful(self, card, hand):
        for current in hand:
            if current.rank == card.rank:
                return True
        value = rank_to_value(card.rank)
        for current in hand:
            if current.suit == card.suit and abs(rank_to_value(current.rank) - value) == 1:
                return True
        return False

    def _computer_meld(self):
        for meld_type in ("run", "set"):
            if self._can_make_meld(self.computer_hand.cards, meld_type):
                indices = self._best_meld_indices(self.computer_hand.cards, meld_type)
                if indices:
                    self.create_meld(self.computer_hand, indices, meld_type)
                    break

    def _can_make_meld(self, cards, meld_type):
        if meld_type == "run":
            for i in range(len(cards) - 2):
                group = [cards[i], cards[i + 1], cards[i + 2]]
                if Meld(group).is_run():
                    return True
            return False
        for i in range(len(cards) - 2):
            group = [cards[i], cards[i + 1], cards[i + 2]]
            if Meld(group).is_set():
                return True
        return False

    def _best_meld_indices(self, cards, meld_type):
        best = []
        for start in range(len(cards)):
            group = []
            for end in range(start, len(cards)):
                group.append(cards[end])
                if len(group) >= 3:
                    trial = Meld(group)
                    if meld_type == "run" and trial.is_run():
                        best = [i for i in range(start, end + 1)]
                        return best
                    if meld_type == "set" and trial.is_set():
                        best = [i for i in range(start, end + 1)]
                        return best
        return best

    def player_turn(self):
        print("Your hand:", self.player_hand)
        print("Discard pile top:", self.discard_pile[-1])
        action = input("Draw from stock (S) or discard pile (D)? ").strip().upper()

        if action == "S":
            self.draw_from_stock(self.player_hand)
        elif action == "D":
            self.draw_from_discard(self.player_hand)
        else:
            print("Invalid choice. Drawing from stock by default.")
            self.draw_from_stock(self.player_hand)

        print("Updated hand:", self.player_hand)

        while True:
            decision = input("Create meld (M), lay off (L), or discard (D)? ").strip().upper()
            if decision == "M":
                indices_input = input("Enter card positions to meld (example: 1 2 3): ")
                try:
                    indices = [int(i) - 1 for i in indices_input.split()]
                    kind = input("Run or set? (R/S): ").strip().upper()
                    meld_kind = "run" if kind == "R" else "set"
                    self.create_meld(self.player_hand, indices, meld_kind)
                    break
                except Exception as exc:
                    print(f"Invalid meld: {exc}")
            elif decision == "L":
                if not self.melds:
                    print("No melds available yet.")
                    continue
                for idx, meld in enumerate(self.melds, start=1):
                    print(f"{idx}: {meld}")
                meld_index = int(input("Choose a meld number: ")) - 1
                card_index = int(input("Choose a card in your hand to lay off: ")) - 1
                self.layoff(self.player_hand, self.melds[meld_index], card_index)
                break
            elif decision == "D":
                index = int(input("Choose card number to discard: ")) - 1
                self.discard_card(self.player_hand, index)
                break
            else:
                print("Invalid input. Please try again.")

    def play(self):
        while True:
            if self.turn == "player":
                self.player_turn()
                self.turn = "computer"
            else:
                self.computer_turn()
                self.turn = "player"

            if len(self.player_hand.cards) == 0:
                print("You win!")
                break
            if len(self.computer_hand.cards) == 0:
                print("Computer wins!")
                break


def rank_to_value(rank):
    mapping = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
    }
    return mapping.get(rank, 0)


if __name__ == "__main__":
    game = RummyGame()
    game.play()
