
class loanCalculator:

    def __init__(self, sales_price, down_payment_percentage, annual_nominal_rate, amortization_years, payment_frequency, term_years):
        self.sales_price = sales_price
        self.down_payment_percentage = down_payment_percentage
        self.annual_nominal_rate = annual_nominal_rate
        self.amortization_years = amortization_years
        self.term_years = term_years
        self.payment_frequency = payment_frequency

    def calculate_loan(self):
        loan_amount = float(self.sales_price) * (1 - float(self.down_payment_percentage)/100)
        annual_rate = float(self.annual_nominal_rate) / 100
        amortization_period = int(self.amortization_years) * 12
        term_period = int(self.term_years) * 12                
        payment_frequency = self.payment_frequency

        mortgage_details = self.get_mortgage_details(annual_rate, loan_amount, amortization_period, payment_frequency, term_period)
        amortization_schedule = self.get_amortization_schedule(annual_rate, loan_amount, amortization_period, payment_frequency, term_period)


        
    def get_mortgage_details(self,annual_rate, loan_amount, amortization_period, payment_frequency, term_period):
        effective_rate = (1 + annual_rate / 2) ** 2 - 1
        monthlyEquivRate = (1 + effective_rate) ** (1/12) - 1
        monthlyPayment = (monthlyEquivRate * loan_amount) / (1 - (1 + monthlyEquivRate) ** (-1 * amortization_period))
        number_of_monthly_payments = term_period 
        periodic_rate = 0
        periodic_payment = 0
        number_of_payment = 0
        
        #["monthly", "semiMonthly", "biWeekly", "weekly", "acceleratedBiWeekly", "acceleratedWeekly"]
        if payment_frequency == 'monthly':
            periodic_rate = monthlyEquivRate
            periodic_payment = monthlyPayment
            number_of_payment = number_of_monthly_payments
        elif payment_frequency == 'semiMonthly':
            periodic_rate = (1 + effective_rate) ** (1/24) - 1
            periodic_payment = monthlyPayment / 2
            number_of_payment = number_of_monthly_payments * 2
        elif payment_frequency == 'biWeekly':
            periodic_rate = (1 + effective_rate) ** (1/26) - 1
            periodic_payment = monthlyPayment * 12 / 26
            number_of_payment = number_of_monthly_payments / 12 * 26
        elif payment_frequency == 'weekly':
            periodic_rate = (1 + effective_rate) ** (1/52) - 1
            periodic_payment = monthlyPayment * 12 / 52
            number_of_payment = number_of_monthly_payments / 12 * 52
        elif payment_frequency == 'acceleratedBiWeekly':
            periodic_rate = (1 + effective_rate) ** (1/26) - 1
            periodic_payment = monthlyPayment / 2
            number_of_payment = number_of_monthly_payments * 2
        elif payment_frequency == 'acceleratedWeekly':
            periodic_rate = (1 + effective_rate) ** (1/52) - 1
            periodic_payment = monthlyPayment / 4
            number_of_payment = number_of_monthly_payments * 4
        return {
            'loan_amount':loan_amount,
            'effective_rate': round(effective_rate * 100,4),
            'periodic_rate': round(periodic_rate * 100,4),
            'periodic_payment': round(periodic_payment,2),
            'number_of_payment': number_of_payment
        }
    
    def get_amortization_schedule(self,annual_rate, loan_amount, amortization_period, payment_frequency, term_period):
        schedule = []
        mortgage_details = self.get_mortgage_details(annual_rate, loan_amount, amortization_period, payment_frequency, term_period)
        periodic_payment = mortgage_details['periodic_payment']
        periodic_rate = mortgage_details['periodic_rate'] / 100
        number_of_payment = mortgage_details['number_of_payment']
        balance = loan_amount
        #terms = termPeriod
        period = 0
        
        while True:# and period <= terms:
            if period <= number_of_payment:
                interest = balance * periodic_rate
                payment = periodic_payment
                principal = payment - interest
                starting_balance = balance
                balance = balance - principal

                if balance < 0:
                    payment = payment + principal
                    principal = payment - interest
                    balance = 0
                
                schedule.append({
                    'period': period,
                    'starting_balance': format(starting_balance, '10.2f'),
                    'payment': format(payment, '10.2f'),
                    'principal': format(principal, '10.2f'),
                    'interest': format(interest, '10.2f'),
                    'ending_balance': format(balance, '10.2f')
                })
                if balance == 0:
                    break
                period += 1
            if period > number_of_payment: 
                break
        return schedule
