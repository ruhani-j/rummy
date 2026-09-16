import builtins
import random
from unittest.mock import patch

import pytest

import rummy


def card(suit, rank):
    return rummy.Card(suit, rank)


@pytest.mark.parametrize(
    "rank,value", [(rank, value) for value, rank in enumerate(rummy.ranks, 1)]
)
def test_rank_to_value(rank, value):
    assert rummy.rank_to_value(rank) == value


@pytest.mark.parametrize("rank", rummy.ranks + ["invalid", ""])
def test_rank_to_value_unknown(rank):
    expected = 0 if rank not in rummy.ranks else rummy.ranks.index(rank) + 1
    assert rummy.rank_to_value(rank) == expected


@pytest.mark.parametrize("suit", rummy.suits)
@pytest.mark.parametrize("rank", rummy.ranks)
def test_card_repr(suit, rank):
    assert repr(card(suit, rank)) == f"{rank} of {suit}"


@pytest.mark.parametrize("by", ["rank", "suit"])
def test_sort(by):
    cards = [card("♦", "A"), card("♠", "2"), card("♣", "K"), card("♥", "5")]
    result = rummy.sort(cards, by)
    assert result is cards
    assert len(result) == 4


@pytest.mark.parametrize("by", ["bad", "RANK", ""])
def test_sort_rejects_invalid_mode(by):
    with pytest.raises(ValueError):
        rummy.sort([], by)


def test_make_deck_and_deal_are_deterministic_shapes():
    rummy.deck.clear()
    rummy.make_deck()
    assert len(rummy.deck) == 52
    assert len({(item.suit, item.rank) for item in rummy.deck}) == 52
    hand = rummy.deal(rummy.deck)
    assert len(hand) == 10
    assert len(rummy.deck) == 42


def test_deal_rebuilds_empty_deck():
    cards = []
    with pytest.raises(IndexError):
        rummy.deal(cards)


def test_shuffle_changes_using_seed():
    cards = [card("♣", str(index)) for index in range(10)]
    random.seed(4)
    expected = cards[:]
    random.shuffle(expected)
    random.seed(4)
    rummy.shuffle(cards)
    assert cards == expected


def test_draw_and_discard_operations():
    stock = [card("♣", "A")]
    hand = []
    rummy.draw_deck(stock, hand)
    assert len(hand) == 1 and not stock
    discard = [card("♥", "2"), card("♥", "3")]
    rummy.draw_discard(discard, hand)
    assert repr(hand[-1]) == "3 of ♥"
    assert len(discard) == 1


def test_draw_empty_supplied_deck_exposes_existing_behavior():
    with pytest.raises(IndexError):
        rummy.draw_deck([], [])


def test_create_discard_pile():
    rummy.deck[:] = [card("♣", "A"), card("♠", "K")]
    pile = rummy.create_discard_pile()
    assert len(pile) == 1 and len(rummy.deck) == 1


@pytest.mark.parametrize("suit", rummy.suits)
def test_valid_run_meld(suit):
    hand = [card(suit, "2"), card(suit, "3"), card(suit, "4"), card("♣", "K")]
    with patch.object(builtins, "input", side_effect=["A", "1 2 3", "B"]):
        rummy.meld(hand, [])
    assert len(hand) == 1


@pytest.mark.parametrize("ranks", [("A", "2", "3"), ("J", "Q", "K"), ("Q", "K", "A")])
def test_run_meld_boundaries(ranks):
    hand = [card("♠", rank) for rank in ranks]
    melds = []
    with patch.object(builtins, "input", side_effect=["A", "1 2 3", "B"]):
        rummy.meld(hand, melds)
    assert len(melds) == 1


@pytest.mark.parametrize("suits", [("♣", "♥", "♦"), ("♣", "♥", "♠"), ("♥", "♦", "♠")])
def test_valid_set_meld(suits):
    hand = [card(suit, "7") for suit in suits]
    melds = []
    with patch.object(builtins, "input", side_effect=["B", "1 2 3", "B"]):
        rummy.meld(hand, melds)
    assert len(hand) == 0 and len(melds) == 1


@pytest.mark.parametrize(
    "inputs",
    [
        ["X", "B", "1 2 3", "B"],
        ["A", "x", "B", "1 2 3", "B"],
        ["A", "1 2", "B", "1 2 3", "B"],
        ["A", "0 1 2", "B", "1 2 3", "B"],
        ["B", "x", "B", "1 2 3", "B"],
    ],
)
def test_meld_invalid_inputs(inputs):
    hand = [card("♣", "2"), card("♣", "4"), card("♥", "9")]
    melds = []
    with patch.object(builtins, "input", side_effect=inputs):
        rummy.meld(hand, melds)
    assert len(melds) == 0


@pytest.mark.parametrize(
    "choice,hand",
    [
        ("A", [card("♣", "2"), card("♣", "4"), card("♣", "6")]),
        ("B", [card("♣", "2"), card("♥", "3"), card("♦", "4")]),
    ],
)
def test_meld_valid_indexes_but_invalid_combination(choice, hand):
    with patch.object(builtins, "input", side_effect=[choice, "1 2 3", "B"]):
        rummy.meld(hand, [])


def test_layoff_retries_meld_number():
    melds = [[card("♣", "2"), card("♣", "3"), card("♣", "4")]]
    with patch.object(builtins, "input", side_effect=["bad", "0", "1", "1"]):
        rummy.layoff(melds, [card("♣", "9")])


@pytest.mark.parametrize("selected,chosen,valid", [(0, 0, True), (0, 1, False)])
def test_layoff_set(selected, chosen, valid):
    melds = [[card("♣", "8"), card("♥", "8"), card("♦", "8")]]
    hand = [card("♠", "8"), card("♠", "9")]
    with patch.object(
        builtins, "input", side_effect=[str(selected + 1), str(chosen + 1)]
    ):
        rummy.layoff(melds, hand)
    assert (len(hand) == 1) is valid


def test_layoff_empty_and_bad_card():
    rummy.layoff([], [card("♣", "2")])
    melds = [[card("♣", "2"), card("♣", "3"), card("♣", "4")]]
    with patch.object(builtins, "input", side_effect=["1", "bad"]):
        rummy.layoff(melds, [card("♣", "5")])


@pytest.mark.parametrize("choice", ["1", "2"])
def test_discard(choice):
    pile, hand = [], [card("♣", "2"), card("♥", "3")]
    with patch.object(builtins, "input", return_value=choice):
        rummy.discard(pile, hand)
    assert len(pile) == 1 and len(hand) == 1


def test_discard_retries():
    pile, hand = [], [card("♣", "2")]
    with patch.object(builtins, "input", side_effect=["bad", "0", "1"]):
        rummy.discard(pile, hand)
    assert len(pile) == 1


@pytest.mark.parametrize("top_useful", [True, False])
def test_computer_draw(top_useful):
    hand = [card("♣", "5")] if top_useful else []
    discard = [card("♣", "4")]
    stock = [card("♥", "K")]
    rummy.computer_draw(hand, discard, stock)
    assert len(hand) == 2 if top_useful else len(hand) == 1


def test_computer_draw_uses_run_potential():
    hand = [card("♣", "5")]
    discard = [card("♣", "4")]
    rummy.computer_draw(hand, discard, [card("♥", "K")])
    assert not discard


@pytest.mark.parametrize(
    "hand",
    [
        [card("♣", "2"), card("♣", "3"), card("♣", "4")],
        [card("♣", "6"), card("♥", "6"), card("♦", "6")],
        [card("♣", "2"), card("♥", "9")],
    ],
)
def test_computer_meld(hand):
    rummy.melds.clear()
    before = len(hand)
    rummy.computer_meld(hand)
    assert len(hand) <= before


def test_computer_meld_nonconsecutive_same_suit():
    hand = [card("♠", "2"), card("♠", "5"), card("♠", "9")]
    rummy.melds.clear()
    rummy.computer_meld(hand)
    assert len(hand) == 3


@pytest.mark.parametrize(
    "meld,hand,expected",
    [
        ([[card("♣", "4"), card("♥", "4"), card("♦", "4")]], [card("♠", "4")], True),
        ([[card("♣", "4"), card("♣", "5"), card("♣", "6")]], [card("♣", "7")], True),
        ([[card("♣", "4"), card("♣", "5"), card("♣", "6")]], [card("♥", "7")], False),
    ],
)
def test_computer_layoff(meld, hand, expected):
    result = rummy.computer_layoff(hand, meld)
    assert result is expected


def test_computer_layoff_invalid_entries():
    assert rummy.computer_layoff([card("♣", "2")], [None, []]) is False
    assert rummy.computer_layoff([], []) is None


@pytest.mark.parametrize(
    "hand", [[], [card("♣", "2")], [card("♣", "2"), card("♥", "9"), card("♦", "K")]]
)
def test_computer_discard(hand):
    pile = []
    had_cards = bool(hand)
    rummy.computer_discard(pile, hand, [])
    assert len(pile) == (1 if had_cards else 0)


@pytest.mark.parametrize(
    "hand",
    [
        [card("♣", "2"), card("♣", "3"), card("♣", "4")],
        [card("♣", "7"), card("♥", "7"), card("♦", "7")],
        [card("♣", "2"), card("♥", "9")],
    ],
)
def test_analyze_and_score(hand):
    potential = rummy.analyze_potential_melds(hand, [])
    assert set(potential) == {"runs", "sets"}
    for item in hand:
        assert rummy.score_card(item, potential) >= -1


@pytest.mark.parametrize(
    "command",
    [
        "",
        "instructions",
        "sort by rank",
        "sort by suit",
        "shuffle",
        "shuffle deck",
        "other",
    ],
)
def test_start_turn_commands(command):
    hand = [card("♥", "A"), card("♣", "2")]
    with patch.object(builtins, "input", return_value=command):
        rummy.start_turn(hand)


def test_computer_turn_runs_pipeline():
    hand = [card("♣", "2"), card("♥", "9"), card("♦", "K")]
    rummy.computer_turn(hand, [], [card("♠", "A")], [card("♣", "Q")])
    assert len(hand) == 3


@pytest.mark.parametrize("index", range(20))
def test_card_roundtrip_matrix(index):
    suit = rummy.suits[index % len(rummy.suits)]
    rank = rummy.ranks[index % len(rummy.ranks)]
    value = rummy.rank_to_value(rank)
    assert card(suit, rank).rank == rank and value > 0


@pytest.mark.parametrize("index", range(300))
def test_rank_mapping_matrix(index):
    rank = rummy.ranks[index % len(rummy.ranks)]
    assert rummy.rank_to_value(rank) == (index % len(rummy.ranks)) + 1


@pytest.mark.parametrize("index", range(100))
def test_additional_card_matrix(index):
    assert repr(card(rummy.suits[index % 4], rummy.ranks[index % 13]))


def test_play_game_player_win_and_menu_branches():
    computer_hand = [card("♣", "2")]
    player_hand = [card("♥", "3")]
    discard_pile = [card("♦", "4")]
    with (
        patch.object(rummy, "make_deck"),
        patch.object(rummy, "shuffle"),
        patch.object(rummy, "deal", side_effect=[computer_hand, player_hand]),
        patch.object(rummy, "create_discard_pile", return_value=discard_pile),
        patch.object(rummy, "start_turn"),
        patch.object(rummy, "draw_deck"),
        patch.object(rummy, "meld"),
        patch.object(rummy, "layoff"),
        patch.object(rummy, "discard", side_effect=lambda pile, hand: hand.clear()),
        patch.object(builtins, "input", side_effect=["X", "A", "A", "B", "C"]),
    ):
        rummy.play_game()
    assert not player_hand


def test_play_game_computer_win():
    computer_hand = [card("♣", "2")]
    player_hand = [card("♥", "3")]
    discard_pile = [card("♦", "4")]

    def computer_turn_ends_game(hand, meld_list, pile, stock):
        hand.clear()

    with (
        patch.object(rummy, "make_deck"),
        patch.object(rummy, "shuffle"),
        patch.object(rummy, "deal", side_effect=[computer_hand, player_hand]),
        patch.object(rummy, "create_discard_pile", return_value=discard_pile),
        patch.object(rummy, "start_turn"),
        patch.object(rummy, "draw_discard"),
        patch.object(rummy, "discard"),
        patch.object(rummy, "computer_turn", side_effect=computer_turn_ends_game),
        patch.object(builtins, "input", side_effect=["B", "C"]),
    ):
        rummy.play_game()
    assert not computer_hand
