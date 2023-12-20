from flask import Flask, render_template, request, redirect, url_for, flash
import random
import string


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SECRET_KEY'] = '1111'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/medsync_db'  # Replace with your database name and password if any
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '1111'  # Change this to a random secret key

# Define models
class Patient(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    identification_number = db.Column(db.String(20), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    date_of_birth = db.Column(db.String(10))
    region = db.Column(db.String(50))
    city = db.Column(db.String(50))

    def generate_unique_id(self):
        # Generate a unique ID (for demonstration purposes)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Routes
@app.route('/')
def index():
    return render_template('landing_page.html')

@app.route('/medical_practitioner', methods=['GET', 'POST'])
def medical_practitioner():
    if request.method == 'POST':
        # Handle login logic here
        license = request.form.get('license')
        password = request.form.get('password')
        consent = request.form.get('consent')

        # Implement your authentication logic here (e.g., check against database)
        # For now, let's just print the values
        print(f"License: {license}, Password: {password}, Consent: {consent}")

        flash('Login logic goes here', 'info')
        # Redirect to the patient_home route upon successful login
        return redirect(url_for('patient_home', username='Austin'))
    return render_template('medical_practitioner.html')

@app.route('/handle_patient_unid', methods=['POST'])
def handle_patient_unid():
    if request.method == 'POST':
        patient_unid = request.form.get('patient_unid')
        # Add logic to handle patient UNid (e.g., retrieve patient details from the database)
        print(f"Patient's UNid: {patient_unid}")
        return redirect(url_for('patient_home', username='PatientName'))  # Redirect to patient home with a placeholder name
    return redirect(url_for('medical_practitioner'))

@app.route('/patient_home/<username>')
def patient_home(username):
    # Fetch Diagnostics data for the patient
    diagnostics_data = []  # Assuming diagnostics_data is a list, replace this with your desired data retrieval logic
    return render_template('patient_home.html', username=username, diagnostics_data=diagnostics_data)

@app.route('/add_new_patient', methods=['POST'])
def add_new_patient():
    if request.method == 'POST':
        # Handle new patient registration logic here
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        identification_number = request.form['identification_number']
        phone_number = request.form['phone_number']
        date_of_birth = request.form['date_of_birth']
        region = request.form['region']
        city = request.form['city']

        new_patient = Patient(
            first_name=first_name,
            last_name=last_name,
            identification_number=identification_number,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            region=region,
            city=city
        )

        flash('New Registration Confirmed. Unique Identifier: {}'.format(new_patient.id), 'success')

    return redirect(url_for('medical_practitioner'))

class Diagnostics:
    pass  # Placeholder for Diagnostics class; you can add any required functionality here

if __name__ == '__main__':
    app.run(debug=True)