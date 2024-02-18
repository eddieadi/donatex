from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import stripe
import os
import random
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/donatex'
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_51OkutTSAfG0sO6UDRPf6XVcWDnhv55OavY5ghevZVlDoZdIq4JRm1jSdtgeiAWdoIEenmrTKuLCJIwmRfCf0asXI00SyhRNg7z")
db = SQLAlchemy(app)
users = {}


# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Extract user details
    name = data.get('name')
    email = data.get('email')
    mobile = data.get('mobile')

    # Create a new user
    new_user = User(name=name, email=email, mobile=mobile)

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})


# Mock OTP generator function
def generate_otp():
    return str(random.randint(1000, 9999))

# class SendOTP(Resource):
@app.route('/send-otp', methods=['POST'])
def post(self):
    mobile_number = request.json.get('mobile_number')

    if not mobile_number:
        return jsonify({'error': 'Mobile number is required'}), 400

    # Generate OTP and store in the database
    otp = generate_otp()
    users[mobile_number] = {'otp': otp}

    # In a real-world scenario, you would send the OTP via SMS to the user's mobile number
    # Here, we'll just return the OTP for demonstration purposes
    return jsonify({'otp': otp})

# class VerifyOTP(Resource):
@app.route('/verify-otp', methods=['POST'])
def post(self):
    mobile_number = request.json.get('mobile_number')
    otp_attempt = request.json.get('otp')

    if not mobile_number or not otp_attempt:
        return jsonify({'error': 'Mobile number and OTP are required'}), 400

    # Check if the mobile number exists in the database
    if mobile_number not in users:
        return jsonify({'error': 'Mobile number not found'}), 404

    # Verify OTP
    stored_otp = users[mobile_number]['otp']
    if otp_attempt == stored_otp:
        # In a real-world scenario, you would generate and return an authentication token here
        return jsonify({'message': 'OTP verified successfully'})
    else:
        return jsonify({'error': 'Invalid OTP'}), 401


# Set your Stripe API key

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        # Get the amount from the request payload
        amount = int(request.json.get('amount'))

        # Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',  # Change to your desired currency code
        )
        return jsonify({'client_secret': intent.client_secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/capture-payment', methods=['POST'])
def capture_payment():
    try:
        order_id = request.json.get('order_id')
        payment_id = request.json.get('payment_id')
        
        # Retrieve payment intent to get the amount and name
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)

        # Capture the payment
        stripe.PaymentIntent.capture(payment_id)

        # Save successful payment to the database
        payment = Payment(name=payment_intent.charges.data[0].billing_details.name,
                          amount=payment_intent.charges.data[0].amount_received / 100)  # Convert from cents
        db.session.add(payment)
        db.session.commit()

        return jsonify({'message': 'Payment captured and saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-payment-history/<int:user_id>', methods=['GET'])
def get_payment_history(user_id):
    try:
        payments = Payment.query.filter_by(id=user_id).all()
        payment_data = [{'amount': payment.amount, 'timestamp': payment.timestamp} for payment in payments]
        return jsonify({'payments': payment_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
