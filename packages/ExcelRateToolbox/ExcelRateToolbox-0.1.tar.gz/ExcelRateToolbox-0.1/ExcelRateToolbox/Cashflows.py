import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Cashflows:
    
    def __init__(self, NPER=10, PMT=-105, PV=100,FV=0, irate = 0.10, verbose=False):
    
        """ Generic Cashflows class for calculating interest rates based on the 
        number of periods, interest rate, present value, future value, and 
        fixed payment.
    
        Attributes:
            NPER (int) Total number of periods of the fixed payment
            PMT (float) The total payment amount assumed to occur at the end of 
                        a period
            PV (float) The present value of the item being paid
            FV (float) The future value of the item after the fixed number and 
                        amount of payments
            irate (float) The guess for the actual interest rate (bounded by 
                        0 and 1 - with a default value of 0.10 if not guess 
                        provided)
            verbose (Boolean) If True then displays verbose iteration level 
                        output (default is False)
            """
        
        self.irate = irate
        self.NPER = NPER
        self.PMT = PMT
        self.PV = PV
        self.FV = FV
        self.verbose = verbose

        # Instantiate empty pandas dataframe
        self.data = pd.DataFrame(columns = ['Time', 'PV', 'FV', 'PMT', 'Total',
        'Running_Total'], index = range(1, NPER + 2))
    
    def calculate_rate(self):
        """ Method to iteratively calculate the interest rate via the selected 
            method (with Newton-Raphson as the default)

        Args: 
			opt_method (string) under consideration but not implemented - 
            provides the ability to toggle optimization routines to higher
            order optimization routines (likely Householder's methods)
		
		Returns: 
			float: The correct rate as specified by NPER, PMT, PV, FV

        """
        NPER = self.NPER
        PMT = self.PMT
        PV = self.PV
        FV = self.FV
        Rate = self.irate
        displayIter = self.verbose

        # Algorithm implementation
        cnt = 0
        threshold = 1e-6
        cntmax = 25
        tol = threshold
        
        while (cnt < cntmax and tol >= threshold):
            cnt = cnt + 1
            f = FV/((1 + Rate) ** (NPER)) + PV
            dfdi = FV*(-NPER)*(1 + Rate) ** (-NPER - 1)
            for j in range(NPER):
                j1 = j + 1
                f = f + PMT/((1 + Rate) ** j1)
                dfdi = dfdi + PMT*(-j1)/((1 + Rate) ** (j1-1))
            if displayIter:
                print('Iteration = {}, Objective = {}, Derivative Obj. = {}, Tolerance = {}'.format(cnt, f, dfdi, abs(f)))
            Rate = Rate - f/dfdi
            tol = abs(f)

        # Generate the self.data dataframe
        self.data['Time'] = range(1, NPER+2)
        self.data['Time'] = self.data['Time'].subtract(1)

        # Setup the PV value
        self.data['PV'] = 0.0
        self.data.iloc[0,self.data.columns.get_loc('PV')] = PV

        # Setup the FV values
        self.data['FV'] = 0.0
        self.data.iloc[NPER,self.data.columns.get_loc('FV')] = FV

        # Set payment values
        self.data['PMT'] = PMT
        self.data.iloc[0,self.data.columns.get_loc('PMT')] = 0.0

        # Calculate the totals for all columns
        self.data['Total'] = self.data['PV'] + self.data['FV'] + self.data['PMT']
        
        self.irate = Rate
        return self.irate

    def __repr__(self):
    
        """Function to output the characteristics of the rate calculation
        
        Args:
            None
        
        Returns:
            string: characteristics of the rate calculation
        
        """
        
        RetString = "A rate of {:1.4f} was calculated for {} payment periods with a payment of ${} with a start PV of ${} and ending future value of ${}".\
        format(self.irate, self.NPER, self.PMT, self.PV, self.FV)
        
        RetString = "\t\t\t\t\t   Calculated rate: {:1.4f}% \n \
            Payment periods: {}  \n \
              Fixed payment: ${:.2f}  \n \
              Present value: ${:.2f}  \n \
               Future value: ${:.2f}  \n \
                \n".\
        format(self.irate*100, self.NPER, self.PMT, self.PV, self.FV)
        
        return RetString

    def plot_cashflows(self):
        """Function to output a plot of the series of cashflows.
		
		Args:
			None
			
		Returns:
			None
		"""

        # Generate the plot
        width = 0.35       # the width of the bars: can also be len(x) sequence
        fig, ax = plt.subplots()
        labels = self.data['Time']

        ax.bar(labels, self.data['PV'], width, label='Present Value')
        ax.bar(labels, self.data['PMT'], width, bottom=self.data['PV'],label='Payment')
        ax.bar(labels, self.data['FV'], width, bottom=self.data['PMT'],label='Future Value')
        ax.set_ylabel('Dollars')
        ax.set_title('The return rate for this series of cashflows is {}%'.format(round(self.irate*100,2)))
        ax.legend()
        plt.show()

        pass