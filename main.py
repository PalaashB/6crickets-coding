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
num_simulations = 10001
percentiles = [1, 5, 20, 50, 80, 95, 99]


def simulate_final_amounts(low, high, years, num_simulations=num_simulations, starting_amount=starting_amount):
    factor_matrix = rng.uniform(low=low, high=high, size=(num_simulations, years))
    final_amounts = starting_amount * factor_matrix.prod(axis=1)
    final_amounts.sort()
    return final_amounts


def get_percentiles(final_amounts):
    values = []
    for p in percentiles:
        index = int((p / 100) * (len(final_amounts) - 1))
        values.append(final_amounts[index])
    return values


# One row per (asset, years) case, ready to be written to a csv
header = ["asset", "years"] + [f"p{p}" for p in percentiles]
rows = []

bounds = {"stocks": (0.7, 1.5), "bonds": (0.9, 1.2)}

# 50 years, plus the delayed-start variants (waiting doesn't change anything,
# only the number of invested years matters)
for invest_years in [50, 40, 30, 20, 10]:
    for asset, (low, high) in bounds.items():
        final_amounts = simulate_final_amounts(low=low, high=high, years=invest_years)
        rows.append([asset, invest_years] + get_percentiles(final_amounts))
    