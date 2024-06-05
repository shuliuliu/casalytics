from flask import Flask, render_template, request, redirect, url_for, jsonify
from loan_calculator import loanCalculator

class casalyticsMain:

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
                amortization_period = int(amortization_years) * 1
                term_period = int(term_years) * 12                

                loan_calculator = loanCalculator(sales_price, down_payment_percentage, annual_nominal_rate, amortization_years, payment_frequency, term_years)
                mortgage_details = loan_calculator.get_mortgage_details(annual_rate, loan_amount, amortization_period, payment_frequency, term_period)
                amortization_schedule = loan_calculator.get_amortization_schedule(annual_rate, loan_amount, amortization_period, payment_frequency, term_period)

            return render_template('loan_calc.html', **mortgage_details,amortization_schedule=amortization_schedule)

        
        
    #run function to start application
    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    casalytics_main = casalyticsMain()
    #call the run method to start the application
    casalytics_main.run()
