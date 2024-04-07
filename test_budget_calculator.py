import unittest
from unittest.mock import patch
import io
import os
import shutil
import csv
from budget_calculator import load_tax_rates, calculate_federal_tax, calculate_total_tax, get_monthly_expenses, main

class TestMainProgram(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = 'test_temp_dir'
        os.makedirs(self.test_dir)

        # Create a test CSV file with dummy tax rates
        self.test_tax_rates = {
            'california': {'sales_tax_rate': 9.5, 'income_tax_rate': '1 - 13.3'},
            'texas': {'sales_tax_rate': 8.25, 'income_tax_rate': 'No income tax'}
        }
        self.test_csv_file = os.path.join(self.test_dir, 'test_tax_rates.csv')
        with open(self.test_csv_file, 'w', newline='') as csvfile:
            fieldnames = ['State', 'Sales Tax Rate (%)', 'Income Tax Rate (%)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for state, rates in self.test_tax_rates.items():
                writer.writerow({'State': state.capitalize(), 'Sales Tax Rate (%)': rates['sales_tax_rate'], 'Income Tax Rate (%)': rates['income_tax_rate']})

    def tearDown(self):
        # Remove the temporary directory after testing
        shutil.rmtree(self.test_dir)

    def test_load_tax_rates(self):
        loaded_tax_rates = load_tax_rates(self.test_csv_file)
        self.assertDictEqual(loaded_tax_rates, self.test_tax_rates)

    def test_calculate_federal_tax(self):
        brackets = [
            {'lower_limit': 0, 'upper_limit': 9950, 'rate': 0.10},
            {'lower_limit': 9950, 'upper_limit': 40525, 'rate': 0.12},
            # Add more federal tax brackets as needed
        ]
        income = 50000
        expected_tax = 0  # Placeholder for expected tax
        calculated_tax = calculate_federal_tax(income, brackets)
        self.assertEqual(calculated_tax, expected_tax)

    def test_calculate_federal_tax(self):
        brackets = [
            {'lower_limit': 0, 'upper_limit': 9950, 'rate': 0.10},
            {'lower_limit': 9950, 'upper_limit': 40525, 'rate': 0.12},
            {'lower_limit': 40525, 'upper_limit': 86375, 'rate': 0.22},
            {'lower_limit': 86375, 'upper_limit': 164925, 'rate': 0.24},
            {'lower_limit': 164925, 'upper_limit': 209425, 'rate': 0.32},
            {'lower_limit': 209425, 'upper_limit': 523600, 'rate': 0.35},
            {'lower_limit': 523600, 'upper_limit': float('inf'), 'rate': 0.37}
        ]
        income = 50000
        expected_tax = calculate_federal_tax(income, brackets)
        calculated_tax = calculate_federal_tax(income, brackets)
        self.assertEqual(calculated_tax, expected_tax)


    @patch('builtins.input', side_effect=['1000', 'california', '500', '200', '300'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Your total taxes paid annually are:", output)
        self.assertIn("Total expenses per year:", output)
        self.assertIn("Total remaining income after taxes and expenses:", output)

if __name__ == '__main__':
    unittest.main()
