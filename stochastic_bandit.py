import numpy as np
import config as c

class stochastic_bandit():

    def __init__(self, no_arms=c.NO_ARMS, std_dev = c.STD_DEV, reward_scale=c.REWARD_SCALE):
        self.no_arms = no_arms
        self.std_dev = std_dev
        self.reward_scale = reward_scale
        self.rewards = np.random.uniform(0, reward_scale, no_arms)
        self.total_reward = 0
        self.mean_rewards = np.zeros(no_arms)
        self.arms_pulled_counter = np.zeros(no_arms)

    def acumulate_reward(self, inst_reward):
        self.total_reward += inst_reward

    def pull_arm(self, arm_index):
        reward = np.random.normal(self.rewards[arm_index], self.std_dev)
        self.arms_pulled_counter[arm_index] += 1
        pulled_arm_count = self.arms_pulled_counter[arm_index]
        self.mean_rewards[arm_index] = self.mean_rewards[arm_index]*(pulled_arm_count-1)/pulled_arm_count + reward*(1/pulled_arm_count)
        self.acumulate_reward(reward)
        print(str(reward)+'€')
        print(str(self.total_reward)+'€')
        return reward


class agent():

    def __init__(self, stochastic_bandit):
        no_arms = stochastic_bandit.no_arms
        self.mean_rewards = np.zeros(no_arms)
        self.arms_pulled_counter = np.zeros(no_arms)