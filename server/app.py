#from crypt import methods
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_bcrypt import generate_password_hash, check_password_hash
from oauthlib.oauth2 import WebApplicationClient
import requests
import re
import configparser
from package import Package
from user import User, WebUser
import shippo
from flask import *
from twilio.rest import Client
import random 
 
app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Chiru1998$'
app.config['MYSQL_DB'] = 'knock_knock'

mysql = MySQL(app)
 
## From https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
## Google log in from https://realpython.com/flask-google-login/ 

app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Configuration
config = configparser.ConfigParser()
config.read('config.cfg')
google_client_id = config.get('GOOGLE', 'GOOGLE_CLIENT_ID')
google_client_secret = config.get('GOOGLE', 'GOOGLE_CLIENT_SECRET')
shipping_client_key = config.get('SHIPPING', 'CLIENT_KEY')

# Input credentials
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", google_client_id)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", google_client_secret)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

shippo.config.api_key = shipping_client_key

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    user = User.get(user_id)
    if user:
        return user

    user = WebUser.get(user_id)
    if user:
        return user
    
    else:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('home'))

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        msg = 'You are already logged in!'
        return jsonify({'msg': msg})
        # return (render_template('index.html', name = current_user.name))
        # return (render_template('login1.html', name = current_user.name))
    else:
        msg = ''

        if request.method == 'POST':
            
            email = request.json['email']
            password = request.json['password']

            if not email or not password:
                msg = 'Incorrect username / password !'
                return jsonify({'msg': msg})

            # Retrieves user from DB
            user = WebUser.check(email)

            # If nothing is returned
            if not user or not check_password_hash(user.H_pass, password):
                msg = 'Incorrect username / password !'
                return jsonify({'msg': msg})
            else: # else logs in user
                login_user(user)
                msg = 'You have successfully logged in!'
                return jsonify({'msg': msg})
                # return render_template('login1.html', name = user.name)
        
        msg = 'You are not logged in'
        return{'msg': msg}
    

################## Two Factor authentication ####################
app.secret_key = 'otp'

@app.route('/getOTP', methods = ['POST'])
def getOTP():

    number = request.form['number']
    val = getOTPApi(number)
    if val:
        return render_template('enterOTP.html')
    

@app.route('/validateOTP', methods = ['POST'])
def validateOTP():
    otp = request.form['otp']
    if 'response' in session:
        s = session['response']
        session.pop('response', None)
        if s == otp:
            return render_template('index.html')
        else:
            return render_template('login.html')
            

def generateOTP():
    return random.randrange(100000, 999999)

def getOTPApi(number):
    account_sid = 'AC852e3620a0b4cb0e4dc7317f8fc38cf8'
    auth_token = '53117afe15ec6dc2e4ce1b632def463d'
    client = Client(account_sid, auth_token)
    otp = generateOTP()
    session['response'] = str(otp)
    body = 'Your OTP is ' + str(otp)
    message = client.messages.create(
        from_='+18884921315',
        body=body,
        to=number
    )

    if message.sid:
        return True
    else:
        False

###########################################

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)
    
 
@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = 'something'
    if request.method == 'POST':
        name = request.json['name']
        password = request.json['password']
        email = request.json['email']
        mobile = request.json['mobile']
        address_line1 = request.json['address_line1']
        city = request.json['city']
        state = request.json['state']
        zip = request.json['zip']
        H_pass = generate_password_hash(password)


        if not name or not password or not email or not mobile or not address_line1 or not city or not state or not zip:
            msg = 'Please fill out the form!'
            #return render_template('register.html', msg = msg)
            return jsonify({name, email, mobile, address_line1, city, state, zip})

        # For checking if user exists already
        user = WebUser.check(email)

        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        
        else:
            # Makes new user and logs it in
            WebUser.create(name, email, H_pass, mobile, address_line1, city, state, zip)
            user = WebUser.check(email)
            login_user(user)
            msg = 'You have successfully registered !'
            return jsonify({'msg': msg})
    
    #return render_template('register.html', msg = msg)
    msg = 'You have successfully registered !'
    return jsonify({'msg': msg})

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return render_template('index.html', name = users_name)  


# Log out, must be logged in
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home')) 

@app.route('/search', methods=['GET', 'POST'])
def search():
    msg = ''
    if request.method == 'POST':
        street1_to = request.form['street1_to']
        street2_to = request.form['street2_to']
        city_to = request.form['city_to']
        state_to = request.form['state_to']
        zip_to = request.form['zip_to']

        street1_from = request.form['street1_from']
        street2_from = request.form['street2_from']
        city_from = request.form['city_from']
        state_from = request.form['state_from']
        zip_from = request.form['zip_from']

        length = request.form['length']
        width = request.form['width']
        height = request.form['height']
        weight = request.form['weight']

        if not street1_to or not city_to or not state_to or not zip_to:
            msg = 'Invalid shipping location'
        elif not street1_from or not city_from or not state_from or not zip_from:
            msg = 'Invalid return location'
        elif not length or not width or not height or not weight:
            msg = 'Missing package information'
        elif not re.match(r'[0-9]+', length) or not re.match(r'[0-9]+', width) or not re.match(r'[0-9]+', height) or not re.match(r'[0-9]+', weight):
            msg = 'Package size and weight must be numbers'
        else:

            # Creates the send to address
            address_to = shippo.Address.create(
                street1 = street1_to,
                street2 = street2_to,
                city = city_to,
                state = state_to,
                zip = zip_to,
                country = "US",
                validate = True
            )

            # Creates the return address
            address_from = shippo.Address.create(
                street1 = street1_from,
                street2 = street2_from,
                city = city_from,
                state = state_from,
                zip = zip_from,
                country = "US",
                validate = True
            )

            # For validation of address
            validate_to = address_to.get('validation_results')
            validate_from = address_from.get('validation_results')

            if not validate_to['is_valid'] and not validate_from['is_valid']:
                msg = 'Return address and send to address is invalid'
                return render_template('search.html', msg = msg)
            elif not validate_to['is_valid']:
                msg = 'Address to send to is invalid'
                return render_template('search.html', msg = msg)
            elif not validate_from['is_valid']:
                msg = 'Return address is invalid'
                return render_template('search.html', msg = msg)
            elif street1_to == street1_from and city_to == city_from and state_to == state_from and zip_to == zip_from:
                msg = 'Addresses need to be the different'
                return render_template('search.html', msg = msg)

            # Creates parcel info for shipping
            parcel = {
                "length": length,
                "width": width,
                "height": height,
                # Distance units can be cm, in, ft, mm, m, yd
                "distance_unit": "in",
                "weight": weight,
                # Mass units can be g, oz, lb, kg
                "mass_unit": "lb",
            }

            # Creates shipments
            shipment = shippo.Shipment.create(
                address_from=address_from,
                address_to=address_to,
                parcels=[parcel],
                asynchronous=False
            )

            # Gets list of rates
            rates = shipment.rates

            for rate in rates:
                if 'BESTVALUE' in rate['attributes']:
                    session['best'] = rate
                    session['orgbest'] = rate

            # Sends rates to be able to be used in html
            session['rates'] = rates
            session['original'] = rates
            session['addrto'] = address_to
            session['addrfrom'] = address_from

            return redirect(url_for('results'))
    elif request.method == 'POST':
        msg = 'Please fill out the form'
    return render_template('search.html', msg = msg)

@app.route('/search/filters', methods=['GET', 'POST'])
def filters():
    rates = session.pop('rates', [])
    filtered = []

    ups = request.form.get('ups')
    fedex = request.form.get('fedex')
    usps = request.form.get('usps')
    less10 = request.form.get('less10')
    tento20 = request.form.get('10to20')
    less3 = request.form.get('less3')
    threeto6 = request.form.get('3to6')

    if ups and not filtered:
        filtered = list(filter(check_ups, rates))
    elif ups and filtered:
        filtered = list(filter(check_ups, filtered))

    if usps and not filtered:
        filtered = list(filter(check_usps, rates))
    elif usps and filtered:
        filtered = list(filter(check_usps, filtered))
    
    if fedex and not filtered:
        filtered = list(filter(check_fedex, rates))
    elif fedex and filtered:
        filtered = list(filter(check_fedex, filtered))

    if less10 and not filtered:
        filtered = list(filter(check_less10, rates))
    elif less10 and filtered:
        filtered = list(filter(check_less10, filtered))

    if tento20 and not filtered:
        filtered = list(filter(check_10to20, rates))
    elif tento20 and filtered:
        filtered = list(filter(check_10to20, filtered))

    if less3 and not filtered:
        filtered = list(filter(check_less3, rates))
    elif less3 and filtered:
        filtered = list(filter(check_less3, filtered))
    
    if threeto6 and not filtered:
        filtered = list(filter(check_3to6, rates))
    elif threeto6 and filtered:
        filtered = list(filter(check_3to6, filtered))

    if not filtered:
        filtered = rates

    session['rates'] = filtered

    # if filter is certain filter return rates
    # Continue for each filter


    return redirect(url_for('results'))

def check_ups(rate):
    if rate['provider'] == 'UPS':
        return True
    
    return False

def check_fedex(rate):
    if rate['provider'] == 'FedEx':
        return True
    
    return False

def check_usps(rate):
    if rate['provider'] == 'USPS':
        return True
    
    return False

def check_less10(rate):
    if float(rate['amount']) < 10:
        return True
    
    return False

def check_10to20(rate):
    if float(rate['amount']) >= 10 and float(rate['amount']) > 20:
        return True
    
    return False

def check_less3(rate):
    if float(rate['estimated_days']) < 3:
        return True
    
    return False

def check_3to6(rate):
    if float(rate['estimated_days']) >= 3 and float(rate['estimated_days']) < 6:
        return True
    
    return False

@app.route('/search/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html')

@app.route('/search/results/reset', methods=['GET', 'POST'])
def reset():
    session['rates'] = session['original']
    session['best'] = session['orgbest']

    return render_template('results.html')

@app.route('/payment/<id>', methods=['GET', 'POST'])
def payment(id):
    return render_template('payment.html', id=id)

@app.route('/payment/confirmation/<id>', methods=['GET', 'POST'])   
def confirmation(id):
    address_to = session.pop('addrto', [])
    address_from = session.pop('addrfrom', [])

    # Get current ID of user and attach package to them
    user_id = current_user.get_id()

    Package.create(user_id, id, address_from, address_to)

    return render_template('confirmation.html', id=id) 

@app.route('/status/<id>', methods=['GET', 'POST'])
def status(id):
    location = Package.get_location(id)
    status = Package.get_status(id)

    return render_template('status.html', location = location, status = status)

@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    tracking = request.form['tracking']

    if not tracking:
        return redirect(url_for('home'))

    return redirect(url_for('status', id=tracking))

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

if __name__ == "__main__":
    app.run(ssl_context="adhoc")

