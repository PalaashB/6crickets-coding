# Investment Outcome Simulation

A Monte Carlo simulation estimating the distribution of outcomes for $1 invested
in stocks, bonds, and a rebalanced mix of the two, over horizons of 10 to 50 years.

## The problem

Under a deliberately crude model of the markets, a dollar invested gets multiplied
each year by a random factor drawn uniformly from a fixed range:

| Asset | Annual factor |
|-------|---------------|
| Stocks | uniform in [0.7, 1.5] |
| Bonds | uniform in [0.9, 1.2] |

The simulation answers four questions:

1. What are the percentile outcomes for $1 in stocks over 50 years?
2. Same for bonds?
3. What if you hold 2/3 stocks and 1/3 bonds, rebalancing to that ratio annually?
4. What if you invest for only 40, 30, 20, or 10 years instead?

Each scenario is run 10,001 times, and the 1st, 5th, 20th, 50th, 80th, 95th, and
99th percentiles of the final dollar amount are reported.

## Requirements

- Python 3
- NumPy

## Usage

```bash
python3 main.py
```

The script writes its results into `results.csv`, filling the empty cells of the
existing table without altering its layout. It reads that file before writing, so
`results.csv` must be present, and the script must be run from the repository root.

## How it works

**One simulated lifetime** is a sequence of annual growth factors multiplied
together. Investing $1 for 50 years means drawing 50 random factors and taking
their product — the final dollar amount.

**Ten thousand and one lifetimes** are simulated at once. Rather than looping,
the code draws a `10001 x years` matrix of random factors and multiplies along
each row, giving 10,001 independent final amounts in a single operation.

**Percentiles** are read off the sorted results by position. With 10,001 sorted
values, the 1st percentile is the value at index 100, the 50th at index 5,000,
and so on. The odd count of 10,001 is deliberate: it makes every percentile land
on an exact index, with no interpolation or rounding needed.

**Rebalancing** works out to a simple weighted average. If you start a year with
amount `A` split 1/3 into bonds and 2/3 into stocks, you end the year with
`(A/3)·bond + (2A/3)·stock`, which is `A · (bond/3 + 2·stock/3)`. So the
portfolio's growth factor for that year is just the weighted average of the two
assets' factors, and those averaged factors compound year over year like any other.
This shortcut is only valid *because* the portfolio is rebalanced annually — without
rebalancing, each asset would have to be compounded separately.

**Delayed starts need no extra code.** Waiting 10 years and then investing for 40
is mathematically identical to investing for 40 years, since the uninvested dollar
does not change while you wait. The 40/30/20/10 year columns therefore answer the
delayed-start question directly.

## Functions

### `simulate_final_amounts(low, high, years)`

Simulates a single-asset investment.

- `low`, `high` — bounds of the uniform annual growth factor (`0.7, 1.5` for
  stocks; `0.9, 1.2` for bonds)
- `years` — length of the investment period

Draws a `num_simulations x years` matrix of random factors, multiplies each row to
get that simulation's final amount, and returns the 10,001 results **sorted
ascending** — ready for percentile lookup by index.

### `simulate_rebalanced_amounts(years)`

Simulates the 2/3 stocks, 1/3 bonds portfolio, rebalanced to that ratio every year.

- `years` — length of the investment period

Draws independent stock and bond factor matrices, combines them into a single
per-year portfolio factor with `(1/3)·bond + (2/3)·stock`, then compounds and
sorts as above. Returns 10,001 sorted final amounts.

### `get_percentiles(final_amounts)`

Extracts the seven reported percentiles from a **sorted** array of outcomes.

- `final_amounts` — sorted results from either simulation function

Returns a list of seven values corresponding to the 1st, 5th, 20th, 50th, 80th,
95th, and 99th percentiles, in that order.

## Parameters

Defined at the top of `main.py`:

| Name | Value | Meaning |
|------|-------|---------|
| `starting_amount` | `1` | Dollars invested at the start |
| `num_simulations` | `10001` | Independent runs per scenario |
| `percentiles` | `[1, 5, 20, 50, 80, 95, 99]` | Percentiles reported |
| `year_options` | `[50, 40, 30, 20, 10]` | Investment horizons simulated |
| `results_file` | `"results.csv"` | Output file |

## Output

`results.csv` uses a fixed two-row header. Each investment horizon occupies three
columns — Stock, Bond, and the 2/3 stock + 1/3 bond mix — and each data row holds
one percentile:

```
,50 year,,,40 year,,,30 year,,,...
,Stock,Bond,2/3 in Stock + 1/3 in Bond,Stock,Bond,...
1%,1.0043,2.4695,2.9921,0.684,1.8802,...
5%,2.9887,3.7071,5.8966,1.7919,2.6417,...
```

Values are the final dollar amount from an initial $1, rounded to four decimals.

Because the random number generator is unseeded, re-running the script produces
slightly different values each time. This is expected — the percentiles are
estimates, and they will shift by small amounts from run to run.

## Tests

```bash
python3 -m unittest test -v
```

The suite covers percentile extraction, the degenerate case of a constant 1.0
growth factor (capital must be preserved exactly), the theoretical bounds of the
rebalanced portfolio, and the structure of the generated CSV.
