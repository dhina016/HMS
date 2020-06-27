__author__ = 'Johannes Gehrs (jgehrs@gmail.com)'

from flask import Flask, render_template, request
from wtforms import Form, validators
import wtformsparsleyjs
import datetime

app = Flask(__name__)


@app.route('/parsley_testform', methods=['GET', 'POST'])
def parsley_testform():
    form = ParsleyTestForm(request.form)
    if request.method == 'POST': form.validate()
    return render_template('wtforms_parsley_sample.html', form=form)


class ParsleyTestForm(Form):
    email = wtformsparsleyjs.EmailField(
        label = 'E-Mail Address',
        validators = [
            validators.Email(
                message = 'Sorrry, not a valid email address.'
            )
        ],
        default='test@example.com'
    )

    ip_address = wtformsparsleyjs.StringField(
        label = 'IP4 Address',
        validators = [
            validators.IPAddress(
                message = 'Sorry, not a valid IP4 Address.'
            )
        ],
        default='127.0.0.1'
    )

    uuid = wtformsparsleyjs.StringField(
        label = 'UUID',
        validators = [
            validators.UUID(
                message = 'Sorry, not a valid UUID.'
            )
        ],
        default='863b5570-ee85-4099-ba1d-33018282cd00'
    )

    mac_address = wtformsparsleyjs.StringField(
        label = 'Mac Address',
        validators = [
            validators.MacAddress(
                message = 'Sorry, not a valid mac address.'
            )
        ],
        default = '10:B0:46:8C:80:48'
    )

    string_length = wtformsparsleyjs.StringField(
        label = 'Length of String (5 to 10)',
        validators = [
            validators.Length(
                message = 'Length should be between 5 and 10 characters.',
                min = 5,
                max = 10
            )
        ],
        default = 'Hello!'
    )

    number_range = wtformsparsleyjs.IntegerField(
        label = 'Number Range (5 to 10)',
        validators = [
            validators.NumberRange(
                message = 'Range should be between 5 and 10.',
                min = 5,
                max = 10
            )
        ],
        default = 7
    )

    required_text = wtformsparsleyjs.StringField(
        label = 'Required Field',
        validators = [
            validators.DataRequired(
                message = 'Sorry, this is a required field.'
            )
        ],
        default = 'Mandatory text'
    )

    required_select = wtformsparsleyjs.SelectField(
        label = 'Required Select',
        validators = [
            validators.DataRequired(
                message = 'Sorry, you have to make a choice.'
            )
        ],
        choices=[
            ('', 'Please select an option'),
            ('cpp', 'C++'),
            ('py', 'Python'),
            ('text', 'Plain Text')
        ],
        default = 'py'
    )

    required_checkbox = wtformsparsleyjs.BooleanField(
        label = 'Required Checkbox',
        validators = [
            validators.DataRequired(
                message = 'Sorry, you need to accept this.'
            )
        ],
        default = True
    )

    regexp = wtformsparsleyjs.StringField(
        label = 'Regex-Matched Hex Color-Code',
        validators = [
            validators.Regexp(
                message = 'Not a proper color code, sorry.',
                regex = r'^#[A-Fa-f0-9]{6}$'
            )
        ],
        default = '#7D384F'
    )

    url = wtformsparsleyjs.StringField(
        label = 'URL Field',
        validators = [
            validators.URL(
                message = 'Sorry, this is not a valid URL,'
            )
        ],
        default = 'http://example.com/parsley'
    )

    anyof = wtformsparsleyjs.StringField(
        'Car, Bike or Plane?',
        validators = [
            validators.AnyOf(
                message = 'Sorry, you can only choose from car, bike and plane',
                values = ['car', 'bike', 'plane']
            )
        ],
        default = 'car'
    )

    date_of_birth = wtformsparsleyjs.DateField(
        label = "Date of birth in the format DD-MM-YYYY",
        format = "%d-%m-%Y",
        validators = [
            validators.InputRequired(
                message = "Sorry this input is required."
            )
        ],
        default = datetime.datetime.today().date()
    )

    date_time = wtformsparsleyjs.DateTimeField(
        label = "Date and time in the format DD/MM/YYYY HH:MM",
        format = "%d/%m/%Y %H:%M",
        validators = [
            validators.InputRequired(
                message = "Sorry this input is required."
            )
        ],
        default = datetime.datetime.today()
    )

    length = wtformsparsleyjs.DecimalField(
        label = "Exact length, as a decimal",
        validators = [
            validators.InputRequired(
                message = "Sorry this input is required."
            )
        ],
        default = 4.20
    )

    txt_file = wtformsparsleyjs.FileField(
        label = "Optional file field, of .txt format",
        validators = [
            validators.Regexp(
                r"^.+\.txt$",
                message="Must be a *.txt file"
            ),
            validators.Optional()
        ]
    )

    float_field = wtformsparsleyjs.FloatField(
        label = "A float value",
        validators = [
            validators.InputRequired(
                message = "Sorry this input is required."
            )
        ],
        default = 4.20
    )

    best_thing_ever = wtformsparsleyjs.RadioField(
        label = "Is this the best thing ever?",
        choices = [
            ("y", "Yes"),
            ("n", "No")
        ],
        validators = [
            validators.InputRequired(
                message = "We need and answer please."
            )
        ],
        default = "y"
    )

    colour = wtformsparsleyjs.SelectField(
        label = "Select your favourite colour.",
        choices = [
            ("red", "Red"),
            ("blue", "Blue"),
            ("green", "Green")
        ],
        validators = [
            validators.InputRequired(
                message = "Sorry this input is required."
            )
        ]
    )

    hobbies = wtformsparsleyjs.SelectMultipleField(
        label = "Select your hobbies: ",
        choices=[
            ("cooking", "Cooking"),
            ("coding", "Coding"),
            ("reading", "Reading"),
            ("fishing", "Fishing"),
            ("sewing", "Sewing")
        ],
        validators = [
            validators.Optional()
        ]
    )

    name = wtformsparsleyjs.StringField(
        label = "Whom would you have me welease?",
        validators = [
            validators.NoneOf(
                ["Roger", "Roderick", "Woger", "Woderick"],
                message = "Ah. We have no Woger and no Woderick"
            )
        ],
        default = "Brian"
    )

    hidden = wtformsparsleyjs.HiddenField(
        label = "Hidden value",
        validators = [
            validators.NumberRange(
                min = 5,
                message = "Must be greater than 5"
            )
        ],
        default = 6
    )

    # No default values for passwords, because the aren't rendered as a safety
    # feature.
    secret = wtformsparsleyjs.PasswordField(
        label = "Enter your secret:",
        validators = [
            validators.InputRequired(
                message = "Sorry this input is required."
            )
        ],
    )

    same_secret = wtformsparsleyjs.PasswordField(
        label = "Enter your secret again: ",
        validators = [
            validators.EqualTo(
                fieldname = "secret",
                message = "Secrets do not match."
            )
        ],
    )

    life_story = wtformsparsleyjs.TextAreaField(
        label = "Tell us your life story...",
        validators = [
            validators.Length(
                min = 50,
                message = "C'mon that's not long enough to be a life story"
            )
        ],
        default = "This is my life story, it has to be at least 50 characters."
    )

    url = wtformsparsleyjs.URLField(
        label = "Enter your website: ",
        default = "crashoverhackthemainframe.c"
    )

    tel = wtformsparsleyjs.TelField(
        label = "Enter your telephone number: ",
        validators = [
            validators.Regexp('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',
                message = "Please enter a valid telephone number e.g. +91 (123) 456-7890"
            )
        ],
        default = "+91 (123) 456-7890 0000000"
    )

    search = wtformsparsleyjs.SearchField(
        label = "Enter your search term: ",
        validators = [
            validators.Length(
                max = 10,
                message = "Search query too long it almost killed our server"
            )
        ],
        default = "How can mirrors be real when our eyes arn't real?"
    )

    decimal_range = wtformsparsleyjs.DecimalRangeField(
        label = "Enter your favorite decimal: ",
        validators = [
            validators.NumberRange(
                message = "That's not your favourite number, it's between 0 and 50",
                min = 0,
                max = 50
            )
        ],
        default = 70,
    )

    ineger_range = wtformsparsleyjs.IntegerRangeField(
        label = "Enter your age (you must be over 18): ",
        validators = [
            validators.NumberRange(
                message = "That's not your age, it's between 3 and 5",
                min = 3,
                max = 5
            ),
        ],
        default = 18
    )
