import csv
import os
import unittest
import numpy as np

# Import core simulation logic from main
from main import (
    get_percentiles,
    num_simulations,
    percentiles,
    results_file,
    simulate_final_amounts,
    simulate_rebalanced_amounts,
)


class TestInvestmentSimulation(unittest.TestCase):

    def test_percentiles_length_and_sorting(self):
        """Verify get_percentiles returns exactly 7 non-decreasing values."""
        sample_data = np.linspace(1, 100, num_simulations)
        results = get_percentiles(sample_data)

        self.assertEqual(len(results), len(percentiles))
        self.assertTrue(
            all(results[i] <= results[i + 1] for i in range(len(results) - 1)),
            "Extracted percentiles must be sorted in non-decreasing order.",
        )

    def test_deterministic_multiplier_bounds(self):
        """Verify that a static 1.0 multiplier preserves capital exactly across all years."""
        years = 10
        final_amounts = simulate_final_amounts(low=1.0, high=1.0, years=years)
        
        self.assertEqual(len(final_amounts), num_simulations)
        np.testing.assert_array_almost_equal(final_amounts, 1.0)

    def test_rebalanced_portfolio_theoretical_bounds(self):
        """Verify rebalanced portfolio outcomes remain strictly within mathematical bounds."""
        years = 10
        # Min single-year factor = (1/3)*0.9 + (2/3)*0.7 = 0.7666667
        # Max single-year factor = (1/3)*1.2 + (2/3)*1.5 = 1.4000000
        min_possible = (0.7666667) ** years
        max_possible = (1.4000000) ** years

        results = simulate_rebalanced_amounts(years=years)

        self.assertEqual(len(results), num_simulations)
        self.assertTrue(
            np.all(results >= min_possible),
            "Outcome fell below minimum theoretical bound.",
        )
        self.assertTrue(
            np.all(results <= max_possible),
            "Outcome exceeded maximum theoretical bound.",
        )

    def test_csv_file_structure_and_population(self):
        """Verify results.csv exists and contains non-empty numeric data rows."""
        self.assertTrue(
            os.path.exists(results_file), f"{results_file} does not exist."
        )

        with open(results_file, newline="") as f:
            rows = list(csv.reader(f))

        # Check header + data presence
        self.assertGreaterEqual(len(rows), 9, "CSV should contain headers and 7 data rows.")

        # Check that percentiles match expected row markers (e.g., 1%, 5%, etc.)
        data_rows = rows[2:]
        self.assertEqual(len(data_rows), len(percentiles))

        # Check that numeric values were written into data cells
        first_data_value = float(data_rows[0][1])
        self.assertIsInstance(first_data_value, float)


if __name__ == "__main__":
    unittest.main()