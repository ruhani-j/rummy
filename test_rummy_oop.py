import pytest

from rummy_oop import Card, Deck, Hand, Meld, RummyGame, rank_to_value


def test_card_repr():
    assert repr(Card("♥", "A")) == "A of ♥"


def test_deck_has_52_unique_cards():
    deck = Deck()
    assert len(deck.cards) == 52
    assert len({(card.suit, card.rank) for card in deck.cards}) == 52


def test_hand_sort_by_rank_and_suit():
    hand = Hand([Card("♦", "A"), Card("♠", "2"), Card("♣", "K"), Card("♥", "5")])
    hand.sort("rank")
    assert [card.rank for card in hand.cards] == ["2", "5", "K", "A"]

    hand.sort("suit")
    assert [card.suit for card in hand.cards] == ["♠", "♣", "♥", "♦"]

    with pytest.raises(ValueError):
        hand.sort("bad")


def test_meld_identifies_runs_and_sets():
    run = Meld([Card("♣", "2"), Card("♣", "3"), Card("♣", "4")])
    assert run.is_run() is True
    assert run.kind == "run"

    set_meld = Meld([Card("♣", "7"), Card("♥", "7"), Card("♦", "7")])
    assert set_meld.is_set() is True
    assert set_meld.kind == "set"


def test_game_starts_with_two_hands_and_discard_pile():
    game = RummyGame()
    assert len(game.player_hand.cards) == 10
    assert len(game.computer_hand.cards) == 10
    assert len(game.discard_pile) == 1
    assert len(game.melds) == 0


def test_layoff_adds_valid_card_to_run():
    game = RummyGame()
    meld = Meld([Card("♣", "2"), Card("♣", "3"), Card("♣", "4")])
    hand = Hand([Card("♣", "5")])
    game.layoff(hand, meld, 0)
    assert [card.rank for card in meld.cards] == ["2", "3", "4", "5"]
    assert len(hand.cards) == 0


def test_rank_to_value_handles_ace_and_faces():
    assert rank_to_value("A") == 1
    assert rank_to_value("K") == 13
    assert rank_to_value("10") == 10
    assert rank_to_value("Z") == 0
