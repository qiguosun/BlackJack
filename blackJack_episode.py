import numpy as np
import matplotlib.pyplot as plt
import itertools


def player_policy(states):
    total, *_ = states
    if total < 20:
        return "hit"
    return "stick"


class blackJack_episode():
    def __init__(self, policy=player_policy):
        self.policy = policy
        self.states = []
        self.actions = []
        self.rewards = []
        self.cards = np.minimum(np.arange(1, 14), 10)
        self.D_up, self.D_down = self.cards_D = np.random.choice(
            self.cards, size=2)
        self.cards_P = np.random.choice(self.cards, size=2)

    # make players points exceeds 11

    def initialise(self, pair):
        current_sum = pair.sum()
        usable_ace = False

        if (pair == 1).any():
            current_sum += 10
            usable_ace = True

        # While < 11, ace is usable
        while current_sum < 11:
            deal = np.random.choice(self.cards)
            current_sum += deal
            if deal == 1:
                current_sum += 10
                usable_ace = True

        # Since < 12, won't go bust adding any card (ace counted as 1)
        # since max card value is <= 10
        if current_sum == 11:
            current_sum += np.random.choice(self.cards)

        return current_sum, usable_ace

    def hit(self, current_sum, usable_ace):
        current_sum += np.random.choice(self.cards)
        if current_sum > 21 and usable_ace:
            current_sum -= 10
            usable_ace = False
        return current_sum, usable_ace

    def play(self):
        if set(self.cards_P) == {1, 10}:
            self.states.append((21, self.D_up, True))  # natural
            self.actions.append('stick')
            if set(self.cards_D) == {1, 10}:
                self.rewards.append(0)
            else:
                self.rewards.append(1)

            return self.states, self.actions, self.rewards
        current_sum_P, usable_ace_P = self.initialise(self.cards_P)
        self.states.append((current_sum_P, self.D_up, usable_ace_P))

        while True:
            current_sum_P, _, usable_ace_P = state = self.states[-1]
            action = self.policy(state)
            self.actions.append(action)
            # player first
            if action == "hit":
                current_sum_P, usable_ace_P = self.hit(
                    current_sum_P, usable_ace_P)
                if current_sum_P > 21:
                    self.rewards.append(-1)
                    break
                else:
                    self.rewards.append(0)
                    self.states.append(
                        (current_sum_P, self.D_up, usable_ace_P))
            # Dealer's turn
            else:
                current_sum_D, usable_ace_D = self.initialise(self.cards_D)
                # Dealer's policy
                while current_sum_D < 17:
                    current_sum_D, usable_ace_D = self.hit(
                        current_sum_D, usable_ace_D)
                if current_sum_D > 21:
                    self.rewards.append(1)
                elif current_sum_D > current_sum_P:
                    self.rewards.append(-1)

                elif current_sum_D == current_sum_P:
                    self.rewards.append(0)

                else:
                    assert current_sum_D < current_sum_P
                    self.rewards.append(1)

                break
        return self.states, self.actions, self.rewards


if __name__ == "__main__":
    game = blackJack_episode()
    S, A, R = episode = game.play()
    print("S", S)
    print("A", A)
    print("R", R)
