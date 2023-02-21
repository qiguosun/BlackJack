import numpy as np
import matplotlib.pyplot as plt
import itertools
from tqdm import autonotebook as tqdm
from blackJack_episode import blackJack_episode


def player_policy(states):
    total, *_ = states
    if total < 20:
        return "hit"
    return "stick"


class BlackJack():
    def __init__(self, policy=player_policy, NUM_EP=2000):
        self.policy = policy
        self.gamma = 1
        self.card_value = range(1, 11)
        self.points = range(12, 22)
        self.usable_ace = [True, False]
        self.states = list(itertools.product(
            self.card_value, self.points, self.usable_ace))
        # FEP: [(10,21,False)...]
        self.value = []
        self.num_episodes = NUM_EP
        self.onePlay = blackJack_episode()

    def first_visit_mc(self):
        num_states = len(self.states)
        V = dict(zip(self.states, np.random.normal(size=num_states)))
        # FEP: {(10,15,True): 0.1,...}
        returns = {state: [] for state in self.states}
        # FEP: {(10,15,True): [],...}

        for episode in tqdm.trange(self.num_episodes):
            # Generate an episode following player policy
            # FEP: S [(12, 7, False), (13, 7, False), (17, 7, False)]
            #      A ['hit', 'hit', 'hit']   R [0, 0, -1]
            episode = self.onePlay.play()
            S_0Tm1, A_0Tm1, R_1T = episode
        # loop each step to calculate average rewards for estimating V
            G = 0
            for t, (St, At, Rtp) in list(enumerate(zip(*episode)))[::-1]:
                G = Rtp + self.gamma*G
                if St not in S_0Tm1[:]:
                    returns[St].append(G)
                    V[St] = np.mean(returns[St])
        return V


if __name__ == "__main__":
    bj = BlackJack()
    value = bj.first_visit_mc()
    fig = plt.figure(figsize=(8, 8))
    for idx, (ne, val) in enumerate(value.items(), 1):
        axis = fig.add_subplot(2, 1, 1, projection='3d')
        X, Y = np.meshgrid(range(1, 11), range(12, 22))
        Z = np.zeros_like(X).astype('float')
        for (cs, sc, ua), v in value.items():
            if ua == False:
                Z[cs-1, sc-12] = v
        axis.plot_wireframe(X, Y, Z, linewidth=0.7, color='k')
        plt.show()
