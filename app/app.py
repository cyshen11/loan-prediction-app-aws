from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, DateField
from wtforms.validators import InputRequired
from autogluon.tabular import TabularPredictor
import pandas as pd
import random
import markdown

# Initialize Flask app
app = Flask(__name__)
# Set a secret key for the form (for security purposes)
app.config["SECRET_KEY"] = str(random.random())


# Define the LoanForm class using Flask-WTF
# This form will handle user input for loan prediction
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
            (None, "Nil"),  # Allow for no card type
        ],
    )
    avg_salary = IntegerField("Monthly Salary", [InputRequired()])
    gender = SelectField("Gender", choices=[("M", "Male"), ("F", "Female")])
    age = IntegerField("Age", [InputRequired()])


# Define the main route for the loan prediction app
@app.route("/", methods=["POST", "GET"])
def loan_prediction_app():
    # Initialize variables for loan status and modal visibility
    loan_status = ""
    show_modal = False
    # Create an instance of the LoanForm
    form = LoanForm()
    # Check if the form has been submitted and is valid
    if form.validate_on_submit():
        # Get the form data and convert it into a pandas DataFrame
        data = get_form_data(request)
        # Predict the loan status using the provided data
        loan_status = predict_loan_status(data)
        # Set the modal to be visible to display the prediction
        show_modal = True
        # Render the template with the form, loan status, and modal visibility
        return render_template(
            "index.html", form=form, loan_status=loan_status, show_modal=show_modal
        )

    # If the form is not submitted or invalid, render the template with the form
    return render_template(
        "index.html", form=form, loan_status=loan_status, show_modal=show_modal
    )

# Define the about route for the loan prediction app
@app.route("/about")
def about():
    with open('../README.md') as f:
        readme_html = markdown.markdown(f.read())
    return render_template(
        "about.html",
        readme_html=readme_html
    )


# Function to extract data from the submitted form
# and convert it into a pandas DataFrame
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
    # Extract data for each field from the form
    for f in fields:
        data[f] = [request.form.get(f)]
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data=data)
    # Calculate the number of days between account creation and loan date
    df["days_between"] = pd.to_datetime(df["loan_date"]) - pd.to_datetime(
        df["account_creation_date"]
    )
    # Drop the original date columns as we now have the difference in days
    df.drop(["account_creation_date", "loan_date"], axis=1, inplace=True)
    # Return the processed DataFrame
    return df


# Function to predict the loan status using a pre-trained model
def predict_loan_status(data):
    # Load the pre-trained TabularPredictor model
    predictor = TabularPredictor.load("./static/model/final")
    # Make a prediction using the provided data
    prediction = predictor.predict(data).iloc[0]
    # Return a user-friendly message based on the prediction

    if prediction == "A":
        return "Loan will be paid off!"
    else:
        return "Loan will not be paid off!"