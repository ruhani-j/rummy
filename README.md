# Rummy Card Game

A terminal-based Rummy card game built in Python.

Created by **Celeste Lopez Boulton** and **Ruhani Jindal** as our final project for CS40S.

---

## How to Play

Run the game from the terminal:

```bash
python rummy.py
```

You play against the computer. Each player is dealt 10 cards, and the goal is to meld your entire hand into valid combinations before your opponent does.

### Melds

- **Run** — 3 or more consecutive cards of the same suit (e.g. 6♥, 7♥, 8♥)
- **Set** — 3 or more cards of the same rank in different suits (e.g. 6♥, 6♠, 6♣)

### Turn Structure

1. Draw a card from the deck or the discard pile
2. Optionally meld cards from your hand or lay off a card onto an existing meld
3. Discard one card to end your turn

The first player to empty their hand wins.

### Commands (at the start of your turn)

| Input | Action |
|---|---|
| *(Enter)* | View your hand |
| `instructions` | Display full rules |
| `sort by rank` | Sort hand by rank |
| `sort by suit` | Sort hand by suit |

---

## Features

- Full 52-card deck with Unicode suit symbols (♣ ♥ ♦ ♠)
- Player vs. computer gameplay
- Smart computer AI that draws, melds, lays off, and discards strategically
- Meld validation for both runs and sets
- Lay off cards onto existing melds (yours or the computer's)
- Score tracking across multiple rounds
- Play again option at the end of each game

---

## Repository Contents

| File | Description |
|---|---|
| `rummy.py` | The game source code |
| `report.pdf` / `report.docx` | Final written report |
| `presentation.pptx` | Project presentation slides |
| `proposal.pdf` / `proposal.docx` | Original project proposal |
| `sources.md` | Sources and references |

---

## Requirements

- Python 3.x
- No external libraries required
