import numpy as np
import matplotlib.pyplot as plt

# True payout % (probabilities of success) of each arm
actual_prob = [0.1, 0.7, 0.5]  # hidden variables in reality

# Counts of success and failure of each arm
succ_fail = [[0,0], [0,0], [0,0]]  # each sub-list contains [num of success, num of failure]

for trial in range(101):
    # Sample a data point (thompson sampling) from all arms' Beta distrib
    samples = [np.random.beta(s+1, f+1) for s, f in succ_fail]  # add 1 because can't pass 0
    
    # Pick the arm with highest sampled estimate
    best_arm = np.argmax(samples)
    
    # Play with best arm
    # since each arm is modelled as bernoulli variable, to sample from bernoulli distribution is same as 
    # sampling a uniform distrib variable & comparing with p (payout), if its less than p, then Success else Failure
    if np.random.uniform() < actual_prob[best_arm]:  
        # if we win with this arm
        succ_fail[best_arm][0] += 1 
    else:
        # if we lose with this arm
        succ_fail[best_arm][1] += 1

    # logging
    if trial % 10 == 0: 
        print(f"trial: {trial}\tsucc_fail: {succ_fail}")


"""
Output:
trial: 0 succ_fail: [[0, 1], [0, 0], [0, 0]]
trial: 10 succ_fail: [[0, 1], [8, 2], [0, 0]]
trial: 20 succ_fail: [[0, 1], [12, 4], [2, 2]]
trial: 30 succ_fail: [[0, 1], [17, 7], [2, 4]]
trial: 40 succ_fail: [[0, 1], [25, 9], [2, 4]]
trial: 50 succ_fail: [[0, 2], [33, 10], [2, 4]]
trial: 60 succ_fail: [[0, 2], [41, 12], [2, 4]]
trial: 70 succ_fail: [[0, 2], [47, 16], [2, 4]]
trial: 80 succ_fail: [[0, 2], [54, 19], [2, 4]]
trial: 90 succ_fail: [[0, 2], [60, 23], [2, 4]]
trial: 100 succ_fail: [[0, 2], [66, 26], [2, 5]]
"""