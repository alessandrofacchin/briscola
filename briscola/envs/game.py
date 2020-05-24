from abc import ABC, abstractmethod
from copy import deepcopy
import enum
import numpy as np
from torch import Tensor
from os import path


class Card(ABC):
    """The class representing a card
    """

    def __init__(self, number: int, suit: int):
        """The constructor of the Agent Class

        :param number (int): number of the card (1: Asso, 10: Re)
        :param suit (int): integer representing the suit of the card (1: denari, 2: coppe, 3: spade, 4: bastoni)

        :attr number (BriscolaNumber):
            number of the card
        :attr suit (BriscolaSuit):
            suit of the card
        """

        self.number = BriscolaNumber(number)
        self.suit = BriscolaSuit(suit)
        self.points = self.number.get_value()

    def is_briscola(self, env) -> bool:
        if self.suit == env.briscola:
            return True
        return False

    def is_liscio(self) -> bool:
        if self.number.value in [2, 4, 5, 6, 7]:
            return True
        return False

    def is_carico(self) -> bool:
        if self.number.value in [1, 3]:
            return True
        return False

    def is_punti(self) -> bool:
        if self.number.value in [1, 3, 8, 9, 10]:
            return True
        return False

    def is_figura(self) -> bool:
        if self.number.value in [8, 9, 10]:
            return True
        return False

    def get_name(self) -> str:
        return '%s di %s' % (self.number.name, self.suit.name)

    def get_graphic(self) -> str:
        return '%d_%d.JPG' % (self.suit.value, self.number.value)


class Table(ABC):
    """The class representing the environment of the game
    """

    def __init__(self):
        """The constructor of the BriscolaTable  Class

        :attr deck (Card[]):
            cards in deck
        :attr player_1 (Card[]):
            cards of player 1
        :attr player_2 (Card[]):
            cards of player 2
        :attr middle_card (Card):
            card in the middle, determining the briscola
        :attr conquered_1 (Card):
            cards conquered by player 1
        :attr conquered_2 (Card):
            cards conquered by player 2
        """
        self.deck = []
        for suit in range(1, 5):
            for number in range(1, 11):
                self.deck.append(Card(number=number, suit=suit))
        np.random.shuffle(self.deck)
        self.player_1 = [self.deck.pop(0) for x in range(3)]
        self.player_2 = [self.deck.pop(0) for x in range(3)]
        self.middle_card = self.deck[-1]
        self.briscola = self.middle_card.suit
        self.conquered_1 = []
        self.conquered_2 = []
        self.plays = []
        self.points = np.zeros([1, 2])
        self.card_played = None
        self.active_player = np.random.randint(1, 3)
        self.is_terminal_state = False

    def calculate_outcome(self, first_card: Card, second_card: Card) -> int:
        """Calculate outcome of a play

        :param first_card (Card): card of the first player
        :param second_card (Card): card of the second player
        :return (int): returning 1 if first player wins, 2 otherwise
        """
        val_1 = 0
        val_2 = 0

        if first_card.suit == self.briscola:
            val_1 += 12
        if second_card.suit == self.briscola:
            val_2 += 12
        elif second_card.suit != first_card.suit:
            val_2 -= 12

        val_1 += first_card.points
        val_2 += second_card.points

        if val_1 > val_2:
            return 1
        else:
            return 2

    def get_turn(self):
        if self.card_played:
            return 3 - self.starting_player
        else:
            return self.starting_player

    def play_card(self, card_index: int) -> int:
        if self.active_player == 1:
            if card_index >= len(self.player_1):
                card_index = np.random.randint(0, len(self.player_1))
            card = self.player_1[card_index]
        else:
            if card_index >= len(self.player_2):
                card_index = np.random.randint(0, len(self.player_2))
            card = self.player_2[card_index]

        # Remove card from player's hand
        if self.active_player == 1:
            self.player_1 = [c for c in self.player_1 if c.suit != card.suit or c.number != card.number]
        else:
            self.player_2 = [c for c in self.player_2 if c.suit != card.suit or c.number != card.number]

        if not self.card_played:
            # Play on the table
            self.card_played = card
            reward = 0
            self.active_player = 3 - self.active_player
        else:
            # Calculate outcome
            outcome = self.calculate_outcome(self.card_played, card)
            if self.active_player == 1:
                outcome = 3 - outcome

            # Append play
            self.plays.append((outcome, self.card_played, card))

            # Update points and conquered cards, draw again
            points = self.card_played.points + card.points
            if outcome == 1:
                self.points[:, 0] += points
                self.conquered_1.append(self.card_played)
                self.conquered_1.append(card)
            else:
                self.points[:, 1] += points
                self.conquered_2.append(self.card_played)
                self.conquered_2.append(card)

            if outcome == self.active_player:
                reward = points
            else:
                reward = -points

            if not self.deck:
                if not self.player_1 and not self.player_2:
                    self.is_terminal_state = True
            elif outcome == 1:
                self.player_1.append(self.deck.pop(0))
                self.player_2.append(self.deck.pop(0))
                self.active_player = 1
            else:
                self.player_2.append(self.deck.pop(0))
                self.player_1.append(self.deck.pop(0))
                self.active_player = 2
            self.card_played = None
        return reward

    def get_features(self, player: int) -> Tensor:
        used_cards = np.zeros([10, 4])
        middle_card = np.zeros([10, 1])
        hand_cards = np.zeros([10, 4])
        points = np.zeros([1, 2])
        briscola = np.zeros([1, 4])
        last_three_plays = np.zeros([3, 10])
        card_played_by_opponent = np.zeros([10, 4])

        for card in self.conquered_1:
            used_cards[card.number.value - 1, card.suit.value - 1] = 1

        for card in self.conquered_2:
            used_cards[card.number.value - 1, card.suit.value - 1] = 1

        middle_card[self.middle_card.number.value - 1, :] = 1
        briscola[:, self.middle_card.suit.value - 1] = 1

        if player == 1:
            for card in self.player_1:
                hand_cards[card.number.value - 1, card.suit.value - 1] = 1
            points[:, 0] = self.points[:, 0]
            points[:, 1] = self.points[:, 1]
        elif player == 2:
            for card in self.player_2:
                hand_cards[card.number.value - 1, card.suit.value - 1] = 1
            points[:, 0] = self.points[:, 0]
            points[:, 1] = self.points[:, 1]

        if self.card_played:
            if player == 1:
                card_played_by_opponent[self.card_played.number.value - 1, self.card_played.suit.value - 1]
            elif player == 2:
                card_played_by_opponent[self.card_played.number.value - 1, self.card_played.suit.value - 1]

        for i in range(1, 4):
            if len(self.plays) >= i:
                if self.plays[-i][0] == 1:
                    last_three_plays[-i, 0] = 1
                elif self.plays[-i][0] == 2:
                    last_three_plays[-i, 1] = 1
                last_three_plays[-i, 2] = self.plays[-i][1].is_briscola(self)
                last_three_plays[-i, 3] = self.plays[-i][2].is_briscola(self)
                last_three_plays[-i, 4] = self.plays[-i][1].is_liscio()
                last_three_plays[-i, 5] = self.plays[-i][2].is_liscio()
                last_three_plays[-i, 6] = self.plays[-i][1].is_carico()
                last_three_plays[-i, 7] = self.plays[-i][2].is_carico()

        if player == 2:
            last_three_plays_tmp = last_three_plays.copy()
            last_three_plays[:, 0::2] = last_three_plays_tmp[:, 1::2]
            last_three_plays[:, 1::2] = last_three_plays_tmp[:, 0::2]

        features = np.concatenate((used_cards.flatten(), middle_card.flatten(), hand_cards.flatten(), points.flatten(),
                                   briscola.flatten(), last_three_plays.flatten(), card_played_by_opponent.flatten()))
        return Tensor(features)


class BriscolaNumber(enum.Enum):
    Re = 10
    Cavallo = 9
    Fante = 8
    Sette = 7
    Sei = 6
    Cinque = 5
    Quattro = 4
    Tre = 3
    Due = 2
    Asso = 1

    def get_value(self) -> int:
        if self.value in [2, 4, 5, 6, 7]:
            return int(0)
        elif self.value == 1:
            return int(11)
        elif self.value == 3:
            return int(10)
        else:
            return int(self.value - 6)


class BriscolaSuit(enum.Enum):
    Denari = 1
    Coppe = 2
    Spade = 3
    Bastoni = 4
