from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, DateField
from wtforms.validators import InputRequired
from autogluon.tabular import TabularPredictor
import pandas as pd
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = str(random.random())

class LoanForm(FlaskForm):
    district_names = ['Rokycany', 'Louny', 'Strakonice', 'Pribram', 'Hl.m. Praha',
  'Brno - mesto', 'Melnik', 'Prachatice', 'Havlickuv Brod', 'Tachov',
  'Bruntal', 'Zlin', 'Vyskov', 'Kromeriz', 'Pelhrimov',
  'Usti nad Labem', 'Praha - vychod', 'Usti nad Orlici',
  'Litomerice', 'Kutna Hora', 'Frydek - Mistek', 'Cheb', 'Opava',
  'Cesky Krumlov', 'Olomouc', 'Zdar nad Sazavou', 'Ceske Budejovice',
  'Prerov', 'Jicin', 'Semily', 'Benesov', 'Rakovnik', 'Pisek',
  'Brno - venkov', 'Jihlava', 'Tabor', 'Karvina', 'Chrudim',
  'Chomutov', 'Teplice', 'Domazlice', 'Karlovy Vary', 'Kolin',
  'Plzen - jih', 'Kladno', 'Sumperk', 'Nachod', 'Liberec',
  'Ostrava - mesto', 'Vsetin', 'Prostejov', 'Svitavy',
  'Jindrichuv Hradec', 'Blansko', 'Pardubice', 'Hradec Kralove',
  'Most', 'Praha - zapad', 'Trebic', 'Nymburk', 'Decin',
  'Plzen - sever', 'Uherske Hradiste', 'Beroun',
  'Rychnov nad Kneznou', 'Plzen - mesto', 'Novy Jicin', 'Trutnov',
  'Breclav', 'Jesenik', 'Mlada Boleslav', 'Hodonin', 'Ceska Lipa',
  'Znojmo', 'Sokolov', 'Klatovy']
    district_names.sort()
    
    district = SelectField(
        'District',
        validators = [InputRequired()],
        choices=district_names
    )
    balance = IntegerField('Balance', [InputRequired()])
    loan_amount = IntegerField('Loan Amount', [InputRequired()])
    loan_duration = IntegerField('Loan Duration (Months)', [InputRequired()])
    loan_payments = IntegerField('Loan Payments', [InputRequired()])
    last_transaction_date = DateField('Last Transaction Date', [InputRequired()])
    last_transaction_amount = IntegerField('Last Transaction Amount', [InputRequired()])
    daily_transactions = IntegerField('Number of Daily Transactions on Average', [InputRequired()])

@app.route("/", methods=["POST", "GET"])
def loan_prediction_app():    
    loan_status = ""
    show_modal = False
    form = LoanForm()
    if form.validate_on_submit():
        data = get_form_data(request)
        loan_status=predict_loan_status(data)
        show_modal=True
        return render_template(
            'index.html', 
            form=form, 
            loan_status=loan_status,
            show_modal=show_modal
        )
        
    return render_template(
        'index.html', 
        form=form, 
        loan_status=loan_status,
        show_modal=show_modal
    )

def get_form_data(request):
    return pd.DataFrame(data={
        'district_name': [request.form.get('district')],
        'trans_date_latest': [request.form.get('transactions-date')],
        'loan_duration': [request.form.get('loan-duration')],
        'district_name': [request.form.get('district')],
        'loan_payments': [request.form.get('loan-payments')],
        'loan_amount': [request.form.get('loan-amount')],
        'trans_balance_latest': [request.form.get('balance')],
        'median_daily_trans_count_p3m': [request.form.get('daily-transactions')],
        'trans_amount_latest': [request.form.get('transaction-amount')]
    })

def predict_loan_status(data):
    predictor = TabularPredictor.load('./static/model/final')
    prediction = predictor.predict(data).iloc[0]
    
    if prediction == "A":
        return "Loan will be paid off!"
    else:
        return "Loan will not be paid off!"
