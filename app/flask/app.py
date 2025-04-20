from flask import Flask, render_template, url_for, request
from autogluon.tabular import TabularPredictor
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def loan_prediction_app():
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
    
    if request.method == "POST":
        df = get_form_data(request)
        print(df.iloc[0])
        # predict_loan_status()
        
    return render_template('index.html', district_names=district_names)

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

def predict_loan_status():
    predictor = TabularPredictor.load('./static/model/final')