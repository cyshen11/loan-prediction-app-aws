from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, DateField
from wtforms.validators import InputRequired
from autogluon.tabular import TabularPredictor
import pandas as pd
import random
import markdown

app = Flask(__name__)
app.config["SECRET_KEY"] = str(random.random())

class LoanForm(FlaskForm):
    loan_duration = IntegerField("Loan Duration (Months)", [InputRequired()])
    loan_amount = IntegerField("Loan Amount", [InputRequired()])
    loan_payments = IntegerField("Loan Payments", [InputRequired()])
    account_creation_date = DateField("Account Creation Date", [InputRequired()])
    loan_date = DateField("Loan Date", [InputRequired()])
    account_frequency = SelectField(
        "Account Frequency",
        choices=[
            ("POPLATEK MESICNE", "Monthly Issuance"),
            ("POPLATEK TYDNE", "Weekly Issuance"),
            ("POPLATEK PO OBRATU", "Issuance After Transaction"),
        ],
    )
    avg_order_amount = IntegerField(
        "Average Payment Order Amount (based on past 12 months)", [InputRequired()]
    )
    avg_trans_amount = IntegerField(
        "Average Transaction Amount (based on past 12 months)", [InputRequired()]
    )
    avg_trans_balance = IntegerField(
        "Average Transaction Balance (based on past 12 months)", [InputRequired()]
    )
    n_trans = IntegerField(
        "Number of Transactions since Inception", [InputRequired()]
    )
    card_type = SelectField(
        "Card Type",
        choices=[
            ("classic", "Classic"),
            ("gold", "Gold"),
            ("junior", "Junior"),
            (None, "Nil"),
        ],
    )
    avg_salary = IntegerField("Monthly Salary", [InputRequired()])
    gender = SelectField("Gender", choices=[("M", "Male"), ("F", "Female")])
    age = IntegerField("Age", [InputRequired()])


@app.route("/", methods=["POST", "GET"])
def loan_prediction_app():
    loan_status = ""
    show_modal = False
    form = LoanForm()
    if form.validate_on_submit():
        data = get_form_data(request)
        loan_status = predict_loan_status(data)
        show_modal = True
        return render_template(
            "index.html", form=form, loan_status=loan_status, show_modal=show_modal
        )

    return render_template(
        "index.html", form=form, loan_status=loan_status, show_modal=show_modal
    )

@app.route("/about")
def about():
    with open('../../README.md') as f:
        readme_html = markdown.markdown(f.read())
    return render_template(
        "about.html",
        readme_html=readme_html
    )


def get_form_data(request):
    data = {}
    fields = [
        'loan_duration',
        'loan_amount',
        'loan_payments',
        'account_frequency',
        'avg_order_amount',
        'avg_trans_amount',
        'avg_trans_balance',
        'n_trans',
        'card_type',
        'avg_salary',
        'gender',
        'age',
        'loan_date',
        'account_creation_date'
    ]
    for f in fields:
        data[f] = [request.form.get(f)]
    df = pd.DataFrame(data=data)
    df["days_between"] = pd.to_datetime(df["loan_date"]) - pd.to_datetime(
        df["account_creation_date"]
    )
    df.drop(["account_creation_date", "loan_date"], axis=1, inplace=True)
    print(df)
    return df


def predict_loan_status(data):
    predictor = TabularPredictor.load("./static/model/final")
    prediction = predictor.predict(data).iloc[0]
    print(prediction)

    if prediction == "A":
        return "Loan will be paid off!"
    else:
        return "Loan will not be paid off!"