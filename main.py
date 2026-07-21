# Problem:
# Assume a dollar invested in the stock market will, during any year, get multiplied by a random factor uniformly distributed in [0.7, 1.5] (an extremely crude approximation of reality).
# Simulate investing $1 for 50 years.
# Run the simulation 10,001 times to estimate some percentiles of the final dollar outcome distribution:
# 1%, 5%, 20%, 50%, 80%, 95%, 99%
# For the bond market assume the factor is in [0.9, 1.2]. What are the percentiles for $1 invested in bonds for 50 years?
# What if you invest $1/3 in bonds, and $2/3 in stocks, and rebalance to that ratio (1:2) every year?
# What if you wait 10 years before starting, and invest for only 40 years? Or only 30? Or only 20? Or only 10?

import csv
import numpy as np

rng = np.random.default_rng()

# Shared parameters
starting_amount = 1
num_simulations = 10001
percentiles = [1, 5, 20, 50, 80, 95, 99]
year_options = [50, 40, 30, 20, 10]
results_file = "results.csv"


def simulate_final_amounts(low, high, years):
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


def simulate_rebalanced_amounts(years):
    bond_factors = rng.uniform(low=0.9, high=1.2, size=(num_simulations, years))
    stock_factors = rng.uniform(low=0.7, high=1.5, size=(num_simulations, years))
    
    combined_factors = (1/3) * bond_factors + (2/3) * stock_factors
    
    final_amounts = starting_amount * combined_factors.prod(axis=1)
    final_amounts.sort()
    return final_amounts


# Stock, Bond and Rebalanced Sims -----------------



stock_results = {}
bond_results = {}
mix_results = {}

for years in year_options:
    stock_final_amounts = simulate_final_amounts(low=0.7, high=1.5, years=years)
    stock_results[years] = get_percentiles(stock_final_amounts)

    bond_final_amounts = simulate_final_amounts(low=0.9, high=1.2, years=years)
    bond_results[years] = get_percentiles(bond_final_amounts)

    mix_final_amounts = simulate_rebalanced_amounts(years=years)
    mix_results[years] = get_percentiles(mix_final_amounts)


# Fill in results.csv ------------------------

with open(results_file, newline="") as f:
    rows = list(csv.reader(f))

header_rows = rows[:2]
data_rows = rows[2:]

for row_index, row in enumerate(data_rows):
    for year_index, years in enumerate(year_options):
        stock_column = 1 + (year_index * 3)
        bond_column = stock_column + 1
        mix_column = stock_column + 2

        row[stock_column] = round(stock_results[years][row_index], 4)
        row[bond_column] = round(bond_results[years][row_index], 4)
        row[mix_column] = round(mix_results[years][row_index], 4)


with open(results_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(header_rows + data_rows)
