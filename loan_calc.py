from flask import Flask, render_template, request, redirect, url_for, jsonify

class LoanCalculator:

    def __init__(self):
        # Flask(__name__) to create an instance of the Flask class
        # to route URLs to functions, handle HTTP requests, manage configurations.
        self.app = Flask(__name__)
        self.configure_routes()

    # define routes using Flask decorators
    def configure_routes(self):

        # bind the home function to the root URL (/)
        @self.app.route('/')
        def home():
            return render_template('home.html')
        
        @self.app.route('/about')
        def about():
            return render_template('about.html')

        # bind the computePayment function to the /calculate URL with POST requests
        @self.app.route('/calculate_loan', methods=['GET', 'POST'])
        def calculate_loan():
            sales_price = None
            down_payment_percentage = None
            annual_nominal_rate = None
            amortization_years = None
            term_years = None
            payment_frequency = None

            loan_amount = None
            annual_rate = None
            amortization_period = None
            term_period = None
            
            mortgage_details = {}
            amortization_schedule = []

            if request.method == 'POST':
                sales_price = float(request.form['sales_price'])
                down_payment_percentage = float(request.form['down_payment_percentage'])
                annual_nominal_rate = float(request.form['annual_nominal_rate'])
                amortization_years = int(request.form['amortization_years'])
                term_years = int(request.form['term_years'])
                payment_frequency = request.form['payment_frequency']
                
                loan_amount = float(sales_price) * (1 - float(down_payment_percentage)/100)
                annual_rate = float(annual_nominal_rate) / 100
                amortization_period = int(amortization_years) * 12
                term_period = int(term_years) * 12                

                mortgage_details = get_mortgage_details(annual_rate, loan_amount, amortization_period, payment_frequency, term_period)
                amortization_schedule = get_amortization_schedule(annual_rate, loan_amount, amortization_period, payment_frequency, term_period)

            return render_template('loan_calc.html', **mortgage_details,amortization_schedule=amortization_schedule)

        
        def get_mortgage_details(annual_rate, loan_amount, amortization_period, payment_frequency, term_period):
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
        
        def get_amortization_schedule(annual_rate, loan_amount, amortization_period, payment_frequency, term_period):
            schedule = []
            mortgage_details = get_mortgage_details(annual_rate, loan_amount, amortization_period, payment_frequency, term_period)
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
        
    #run function to start application
    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    loan_calculator = LoanCalculator()
    #call the run method to start the application
    loan_calculator.run()
