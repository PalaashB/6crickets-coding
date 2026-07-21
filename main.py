# Problem: 
# Assume a dollar invested in the stock market will, during any year, get multiplied by a random factor uniformly distributed in [0.7, 1.5] (an extremely crude approximation of reality).
# Simulate investing $1 for 50 years.
# Run the simulation 10,001 times to estimate some percentiles of the final dollar outcome distribution:
# 1%, 5%, 20%, 50%, 80%, 95%, 99%
# For the bond market assume the factor is in [0.9, 1.2]. What are the percentiles for $1 invested in bonds for 50 years?
# What if you invest $1/3 in bonds, and $2/3 in stocks, and rebalance to that ratio (1:2) every year?
# What if you wait 10 years before starting, and invest for only 40 years? Or only 30? Or only 20? Or only 10? 

import numpy as np


rng = np.random.default_rng()


matrix = rng.uniform(low=0.7, high=1.5, size=(10001, 50))

amount=1. #starting amount

for sim in matrix:
    sim_amount= amount
    for factor in sim:
        sim_amount= sim_amount*factor
    print(sim_amount)