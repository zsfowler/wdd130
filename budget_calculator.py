import csv
import os

def load_tax_rates(filename):
    try:
        with open(filename, 'r') as file:
            tax_rates = {}
            reader = csv.DictReader(file)
            for row in reader:
                state = row['State']
                sales_tax_rate = float(row['Sales Tax Rate (%)'])
                income_tax_rate = row['Income Tax Rate (%)']
                tax_rates[state.lower()] = {'sales_tax_rate': sales_tax_rate, 'income_tax_rate': income_tax_rate}
        return tax_rates
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the tax rates from '{filename}': {e}")
        return None

def calculate_federal_tax(income, brackets):
    tax = 0
    remaining_income = income
    for bracket in brackets:
        if remaining_income <= 0:
            break
        bracket_amount = min(remaining_income, bracket['upper_limit'] - bracket['lower_limit'])
        tax += bracket_amount * bracket['rate']
        remaining_income -= bracket_amount
    return tax

def calculate_total_tax(income, state, tax_rates, federal_brackets):
    state_info = tax_rates.get(state.lower())
    if not state_info:
        print("State not found in the tax rates data.")
        return None
    sales_tax_rate = state_info['sales_tax_rate']
    income_tax_rate = state_info['income_tax_rate']

    federal_tax = calculate_federal_tax(income, federal_brackets)
    state_income_tax = 0
    if 'No income tax' not in income_tax_rate:
        income_tax_rate = income_tax_rate.split(' - ')
        min_income_tax_rate = float(income_tax_rate[0])
        max_income_tax_rate = float(income_tax_rate[-1])
        state_income_tax = (min_income_tax_rate + max_income_tax_rate) / 2

    total_tax = sales_tax_rate + state_income_tax + federal_tax
    return total_tax

def get_monthly_expenses():
    rent = float(input("Enter your monthly rent cost: $"))
    insurance = float(input("Enter your monthly insurance cost: $"))
    living_expenses = float(input("Enter your monthly living expenses cost: $"))
    return rent, insurance, living_expenses

def main():
    filename = 'state_tax_rates.csv'  # Assuming the CSV file is named 'state_tax_rates.csv'
    current_directory = os.getcwd()
    print("Current working directory:", current_directory)
    file_path = os.path.join(current_directory, filename)
    print("Full file path:", file_path)
    
    tax_rates = load_tax_rates(file_path)
    if tax_rates is None:
        print("Tax rates could not be loaded. Exiting program.")
        return

    # Assuming the federal tax brackets for the year 2022
    federal_brackets = [
        {'lower_limit': 0, 'upper_limit': 9950, 'rate': 0.10},
        {'lower_limit': 9950, 'upper_limit': 40525, 'rate': 0.12},
        {'lower_limit': 40525, 'upper_limit': 86375, 'rate': 0.22},
        {'lower_limit': 86375, 'upper_limit': 164925, 'rate': 0.24},
        {'lower_limit': 164925, 'upper_limit': 209425, 'rate': 0.32},
        {'lower_limit': 209425, 'upper_limit': 523600, 'rate': 0.35},
        {'lower_limit': 523600, 'upper_limit': float('inf'), 'rate': 0.37}
    ]

    income = float(input("Enter your annual income: $"))
    
    # Loop until a valid state is entered
    while True:
        state = input("Enter your state of residence: ").lower()
        if state in tax_rates:
            break
        else:
            print("Invalid state. Please enter a valid state.")

    rent, insurance, living_expenses = get_monthly_expenses()
    
    total_tax = calculate_total_tax(income, state, tax_rates, federal_brackets)
    if total_tax is not None:
        print(f"Your total taxes paid annually are: ${total_tax:.2f}")

    total_expenses_per_year = (rent + insurance + living_expenses) * 12
    total_remaining_income = income - total_tax - total_expenses_per_year
    
    print(f"Total expenses per year: ${total_expenses_per_year:.2f}")
    print(f"Total remaining income after taxes and expenses: ${total_remaining_income:.2f}")

    # Export the annual taxes, income, and expenses to a CSV file
    with open('annual_budget.csv', 'w', newline='') as csvfile:
        fieldnames = ['Income', 'State', 'Total Tax', 'Rent', 'Insurance', 'Living Expenses', 'Total Remaining Income']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Income': income, 'State': state, 'Total Tax': total_tax, 
                         'Rent': rent, 'Insurance': insurance, 'Living Expenses': living_expenses,
                         'Total Remaining Income': total_remaining_income})

    print("Annual budget exported to 'annual_budget.csv'.")

if __name__ == "__main__":
    main()
