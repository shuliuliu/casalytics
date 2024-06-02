from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def calculate_loan(principal, annual_rate, years):
    monthly_rate = annual_rate / 12 / 100
    num_payments = years * 12
    if monthly_rate == 0:
        monthly_payment = principal / num_payments
    else:
        monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -num_payments)
    return monthly_payment

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    monthly_payment = None
    principal = None
    annual_rate = None
    years = None
    if request.method == 'POST':
        principal = float(request.form['principal'])
        annual_rate = float(request.form['annual_rate'])
        years = int(request.form['years'])
        monthly_payment = calculate_loan(principal, annual_rate, years)
    return render_template('index.html', monthly_payment=monthly_payment, principal=principal, annual_rate=annual_rate, years=years)

if __name__ == '__main__':
    app.run(debug=True)
