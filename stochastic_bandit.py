import numpy as np
import config as c

class StochasticBandit():
    """Class defining stochastic bandit environment."""
    def __init__(self, no_arms=c.NO_ARMS, reward_scale=c.REWARD_SCALE, std_dev=c.STD_DEV):
        self.no_arms = no_arms
        self.reward_scale = reward_scale
        self.std_dev = std_dev
        self.rewards = np.random.uniform(c.REWARD_LOW_BOUND, reward_scale, no_arms)

    def pull_arm(self, arm_index):
        """Return noisy reward when certain arm is selected."""
        reward = np.random.normal(self.rewards[arm_index], self.std_dev)
        return reward


class InteractingAgent():
    """Class defining any interacting agent, including actions and policies."""
    def __init__(self, bandit_game):
        self.bandit_instance = bandit_game
        self.no_arms = bandit_game.no_arms
        self.mean_rewards = np.zeros(self.no_arms)
        self.arms_pulled_counter = np.zeros(self.no_arms)
        self.ucb_values = self.mean_rewards + np.infty * np.ones(self.no_arms)
        self.total_reward = 0
        self.no_rounds = 0
        self.alpha_params = np.ones(self.no_arms)
        self.beta_params = np.ones(self.no_arms)

    def acumulate_reward(self, inst_reward):
        """Store total accumulated reward."""
        self.total_reward += inst_reward

    def select_action(self, arm_index):
        """Select an arm within given bandit environment."""
        reward = self.bandit_instance.pull_arm(arm_index)
        self.arms_pulled_counter[arm_index] += 1
        pulled_arm_count = self.arms_pulled_counter[arm_index]
        old_weight = (pulled_arm_count-1)/pulled_arm_count
        new_weight = 1/pulled_arm_count
        self.mean_rewards[arm_index] = self.mean_rewards[arm_index]*old_weight + reward*new_weight
        self.acumulate_reward(reward)
        self.no_rounds += 1
        return reward

    def ucb_policy(self):
        """UCB arm selection policy."""
        arm_index = np.argmax(self.ucb_values)
        self.select_action(arm_index)
        confidence_bound = np.sqrt(2*c.STD_DEV*np.log(1/c.DELTA)/
                                   (self.arms_pulled_counter[arm_index]*self.no_rounds))
        self.ucb_values[arm_index] = self.mean_rewards[arm_index] + confidence_bound

    def ts_policy(self):
        '''TS arm selection policy.'''
        for k in np.arange(self.no_arms):
            sampled_rewards = np.random.beta(self.alpha_params[k], self.beta_params[k])

        arm_index = np.argmax(sampled_rewards)
        reward = self.select_action(arm_index)/c.REWARD_SCALE
        if np.random.uniform(low=c.REWARD_LOW_BOUND/c.REWARD_SCALE) < reward:
            self.alpha_params[arm_index] += 1
            self.beta_params[arm_index] += 1
