import numpy as np
import config as c

class stochastic_bandit():

    def __init__(self, no_arms=c.NO_ARMS, reward_scale=c.REWARD_SCALE, std_dev=c.STD_DEV):
        self.no_arms = no_arms
        self.reward_scale = reward_scale
        self.std_dev = std_dev
        self.rewards = np.random.uniform(0, reward_scale, no_arms)

    def pull_arm(self, arm_index):
        reward = np.random.normal(self.rewards[arm_index], self.std_dev)
        return reward


class agent():

    def __init__(self, bandit_game):
        self.bandit_instance = bandit_game
        self.no_arms = bandit_game.no_arms
        self.mean_rewards = np.zeros(self.no_arms)
        self.arms_pulled_counter = np.zeros(self.no_arms)
        self.total_reward = 0

    def acumulate_reward(self, inst_reward):
        self.total_reward += inst_reward

    def select_action(self, arm_index):
        reward = self.bandit_instance.pull_arm(arm_index)
        self.arms_pulled_counter[arm_index] += 1
        pulled_arm_count = self.arms_pulled_counter[arm_index]
        self.mean_rewards[arm_index] = self.mean_rewards[arm_index]*(pulled_arm_count-1)/pulled_arm_count + reward*(1/pulled_arm_count)
        self.acumulate_reward(reward)

    def ucb_function(self, arm_index):
        pass