# Purpose: store financial equations as functions

# 1. Future Value (Annual Compounding)
# FV = Future Value
# P = Principal
# i = Annual interest rate (decimal)
# n = Number of years
def future_value(P, i, n):
    return round(P * (1 + i) ** n, 2)


# 2. Present Value (Annual Discounting)
# PV = Present Value
# FV = Future Value
# i = Annual discount rate (decimal)
# n = Number of years
def present_value(FV, i, n):
    return round(FV / (1 + i) ** n, 2)


# 3. Future Value with Compound Frequency
# FV = Future Value
# P = Principal
# r = Annual interest rate (decimal)
# n = Compounding frequency per year (e.g., 12 for monthly)
# t = Number of years
def future_value_compounded(P, r, n, t):
    return round(P * (1 + r / n) ** (n * t), 2)

# If $1000 are invested today, in an annual 5% sovereign bond, which pays you quarterly coupons,
# what would be the future value of your investment? Assumption: The coupon payments are invested
# in at the same rate as the sovereign bond

#print(future_value_compounded(1000, 0.05, 4, 1))

# What would be the FV (Future Value) of a $500 investment principal at the end of 7 years, if
# the annual interest rate is 6%?

# print(future_value(500, 0.06, 7))

# Consider you invested $1000 in a monthly coupon bond with a coupon rate of 5%. What would be the future value of your investment after one year?
#
# Assumption: The coupon payments are invested at the same rate (5%).
# Note: Use the equation FV = PV * [( 1 + r/n) ^ (n*t )]. Please use hints if you face any difficulty.

print(future_value_compounded(1000, 0.05, 12, 1))
