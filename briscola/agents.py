from abc import ABC, abstractmethod
import numpy as np
from torch import Tensor


class Agent(ABC):

    def __init__(self):
        self.n_acts = 3
        self.last_action = None
        self.last_obs = None

    @abstractmethod
    def act(self, obs: Tensor, hand_cards, played_card, middle_card):
        ...

    @abstractmethod
    def learn(self, reward, new_obs, hand_cards, played_card, middle_card):
        ...


class RandomAgent(Agent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.policy = Tensor(np.ones([1, 3]) / 3)

    def act(self, obs: Tensor, hand_cards, played_card, middle_card) -> int:
        p = self.policy.detach().numpy()
        action = np.random.choice(range(self.n_acts), p=p.flatten())
        self.last_action = action
        self.last_obs = obs
        return action

    def learn(self, reward, new_obs: Tensor):
        """ This will also use self.last_action and self.last_obs

        :param reward:
        :param new_obs:
        :return:
        """
        pass


class HumanAgent(Agent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_interface = UserInterface()

    def act(self, obs: Tensor, hand_cards, played_card, middle_card) -> int:
        self.user_interface.show_state(hand_cards, played_card, middle_card)
        action = self.user_interface.get_choice()
        self.last_action = action
        self.last_obs = obs
        return action

    def learn(self, reward, new_obs: Tensor):
        """ This will also use self.last_action and self.last_obs

        :param reward:
        :param new_obs:
        :return:
        """
        pass