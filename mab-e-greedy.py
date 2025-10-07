

import numpy as np

class EpsilonGreedy:
    def __init__(self, n_arms, epsilon):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.counts = np.zeros(n_arms)  # Number of times each arm is pulled
        self.values = np.zeros(n_arms)  # Estimated values of each arm

    def select_arm(self):
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, self.n_arms)
        else:
            return np.argmax(self.values)

    def update(self, chosen_arm, reward):
        self.counts[chosen_arm] += 1
        n = self.counts[chosen_arm]
        value = self.values[chosen_arm]
        self.values[chosen_arm] = ((n - 1) / n) * value + (1 / n) * reward

# Example usage
n_arms = 10
epsilon = 0.3
n_trials = 1000
rewards = np.random.randn(n_arms, n_trials)  # Random rewards for demonstration

agent = EpsilonGreedy(n_arms, epsilon)
total_reward = 0

for t in range(n_trials):
    arm = agent.select_arm()
    reward = rewards[arm, t]
    agent.update(arm, reward)
    total_reward += reward

print("Total Reward:", total_reward)