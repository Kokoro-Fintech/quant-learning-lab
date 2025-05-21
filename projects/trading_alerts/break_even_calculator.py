# Purpose: calculate the minimum profit needed in a trade to pay fees and tax

def calculate_break_even():
    # Get user input
    commission = float(input("Enter your commission per trade (in dollars): "))
    tax_rate = float(input("Enter your tax rate (as a percentage, e.g., 28 for 28%): ")) / 100

    # Calculate total commission
    total_commission = commission * 2

    # Calculate break-even profit
    # Let X be the profit needed before tax.
    # After tax, you keep (1 - tax_rate) * X.
    # This must cover your total commission.
    break_even_profit = total_commission / (1 - tax_rate)

    # Display the result
    print(f"\nTo break even after taxes and commission, you need to profit: ${break_even_profit:.2f}")

if __name__ == "__main__":
    calculate_break_even()
