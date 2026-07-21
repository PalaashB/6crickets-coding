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

# Shared parameters
starting_amount = 1
years = 50
num_simulations = 10001
percentiles = [1, 5, 20, 50, 80, 95, 99]



# Stock Sim -----------------

stock_matrix = rng.uniform(low=0.7, high=1.5, size=(num_simulations, years))
stock_final_amounts = []

for stock_sim in stock_matrix:
    current_amount = starting_amount
    for stock_factor in stock_sim:
        current_amount = current_amount * stock_factor
    stock_final_amounts.append(current_amount)

stock_final_amounts.sort()


for p in percentiles:
    index = int((p / 100) * (len(stock_final_amounts) - 1))



# Bond Sim ------------------------

bond_matrix = rng.uniform(low=0.9, high=1.2, size=(num_simulations, years))
bond_final_amounts = []

for bond_sim in bond_matrix:
    current_amount = starting_amount
    for bond_factor in bond_sim:
        current_amount = current_amount * bond_factor
    bond_final_amounts.append(current_amount)

bond_final_amounts.sort()


for p in percentiles:
    index = int((p / 100) * (len(bond_final_amounts) - 1))
    