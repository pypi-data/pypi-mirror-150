# Unit tests for checks
from Cashflows import Cashflows

# Initiation by default and with values
CF1 = Cashflows()
CF1 = Cashflows(49,0,-0.12,492937.5,0.44,False)
CF1.calculate_rate()

# Test calculation from MBA Finance course
print(CF1)

# Investment calculation
CF2 = Cashflows(5,-5.0,-500,600,0.01,False)
CF2.calculate_rate()
print(CF2)

# Generate a plot of the cash flows with calculated rate
CF2.plot_cashflows()

# Mortgage Calculation
CF3 = Cashflows(12*30,-1318.5,291000,0,0.01,False)
CF3.calculate_rate()
print(CF3)

