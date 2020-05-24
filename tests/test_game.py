import pytest
from torch import Tensor
from briscola.envs.game import Card, BriscolaNumber, BriscolaSuit, Table
from briscola.agents import RandomAgent
from briscola.train import play_episode

def test_card():

    card = Card(1, 1)

    assert card.suit == BriscolaSuit.Denari
    assert card.number == BriscolaNumber.Asso
    assert card.points == 11
    assert card.is_carico()
    assert not card.is_figura()
    assert not card.is_liscio()


def test_play():

    # Winning because briscola
    card_1 = Card(2, 1)
    card_2 = Card(1, 2)
    env = Table()
    env.briscola = BriscolaSuit(1)
    assert env.calculate_outcome(card_1, card_2) == 1

    # Losing because lower briscola
    card_1 = Card(2, 1)
    card_2 = Card(1, 1)
    env = Table()
    env.briscola = BriscolaSuit(1)
    assert env.calculate_outcome(card_1, card_2) == 2

    # Winning because different suit
    card_1 = Card(2, 3)
    card_2 = Card(1, 4)
    env = Table()
    env.briscola = BriscolaSuit(1)
    assert env.calculate_outcome(card_1, card_2) == 1

    # Losing because lower number
    card_1 = Card(2, 4)
    card_2 = Card(1, 4)
    env = Table()
    env.briscola = BriscolaSuit(1)
    assert env.calculate_outcome(card_1, card_2) == 2


def test_features():
    table = Table()
    features = table.get_features(1)
    assert isinstance(features, Tensor)


def test_episode():
    a1 = RandomAgent()
    a2 = RandomAgent()
    tab = play_episode(a1, a2)
    assert(isinstance(tab, Table))
