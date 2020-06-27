from flask_wtf import FlaskForm
from wtforms import Form, validators
from wtformsparsleyjs import IntegerField,FloatField, DateField, BooleanField, SelectField, StringField, PasswordField, TextAreaField, RadioField
 



class LoginForm(FlaskForm):
    username   = StringField("Username", [ validators.DataRequired(message="Username is Required"), validators.Length(message='UserName should be Minimun 4 characters.',
                          min=4) ] )
    password = PasswordField("Password", [ validators.DataRequired(message="Password is Required"), validators.Length(message='Password should be and 5 characters.',
                          min=5),validators.Regexp(message=' Password should contain 5 characters including one special character, one upper case, one numeric.',
                          regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[\W\_])[A-Za-z\d\W\_]*$'), ] )

class CreatePatient(FlaskForm):
    ssnid = IntegerField("SSN ID", [validators.DataRequired(message="SSN ID is Required"), validators.NumberRange(message='SSN should be exactly 9', min=100000000, max=999999999) ])
    patientname = StringField("Name", [validators.DataRequired(message="Name is Required"), validators.Regexp(message='Name should only alphabet', regex=r'^[a-zA-Z ]*$') , validators.Length(message='Name should only alphabet and minimum 3 character', min=3, max=25) ] )
    age = IntegerField("Age", [validators.DataRequired(message="Age is Required"), validators.NumberRange(message='Minimum age is 10', min=10, max=120) ])
    address = StringField("Address", [ validators.DataRequired(message="Address is Required") ])
    state = StringField()
    city = StringField()
    type = StringField()

class UpdatePatient(FlaskForm):
    patientid = IntegerField("Patient ID", [validators.DataRequired(message="Patient ID is Required"), validators.NumberRange(message='ID should be exactly 9', min=100000000, max=999999999) ])
    patientname = StringField("Name", [validators.DataRequired(message="Name is Required"), validators.Regexp(message='Name should only alphabet', regex=r'^[a-zA-Z ]*$') , validators.Length(message='Name should only alphabet and minimum 3 character', min=3, max=25) ] )
    age = IntegerField("Age", [validators.DataRequired(message="Age is Required"), validators.NumberRange(message='Minimum age is 10', min=10, max=120) ])
    address = StringField("Address", [ validators.DataRequired(message="Address is Required") ])

class DeletePatient(FlaskForm):
    patientid = IntegerField("Patient ID", [validators.DataRequired(message="Patient ID is Required"), validators.NumberRange(message='ID should be exactly 9', min=100000000, max=999999999) ])

class Medicine(FlaskForm):
    quantity = IntegerField("Quantity", [validators.DataRequired(message="Quantity is Required"), validators.NumberRange(message='Minimum 1', min=1, max=999999999 ) ])
    rate = IntegerField("Rate", [validators.DataRequired(message="Rate is Required"), validators.NumberRange(message='Minimum 1', min=1, max=999999999 ) ])
    medicinename = StringField("Name", [ validators.DataRequired(message="Name is Required") ])

class DeleteMedicine(FlaskForm):
    medicinename = StringField("Name", [ validators.DataRequired(message="Name is Required") ])