## Functional Requirements

### Authentication:

#### APIs:

1. **Register Users:**
   - **Route:** /register
   - **Method:** POST
   - **Description:** Registers users in the system.

2. **Send OTP:**
   - **Route:** /send-otp
   - **Method:** POST
   - **Description:** Sends OTP for user verification.

3. **Verify OTP:**
   - **Route:** /verify-otp
   - **Method:** POST
   - **Description:** Verifies OTP to authenticate users.

---

### Donation Processing:

#### APIs:

1. **Create Payment Intent:**
   - **Route:** /create-payment-intent
   - **Method:** POST
   - **Description:** Initiates the payment process by creating a payment intent.

---

### Payment History Management:

#### APIs:

1. **Capture Payment:**
   - **Route:** /capture-payment
   - **Method:** POST
   - **Description:** Captures the payment and saves the donation details.

---

### Data Visualization:

#### APIs:

1. **Get Payment History:**
   - **Route:** /get-payment-history/<int:user_id>
   - **Method:** GET
   - **Description:** Retrieves donation history for a specific user, allowing for data visualization.

## Steps to Run the Application

### 1. Create the Database in MySQL

```sql
CREATE DATABASE donatex;

USE donatex;

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    mobile VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    amount INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Install Python 3 and Create a Virtual Environment

```bash
# Install Python 3 (if not already installed)
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows, use "venv\Scripts\activate"
```

### 3. Install Required Python Packages

```bash
# Run the following command to install all required Python packages
pip install -r requirements.txt
```

### 4. Run the Flask App

```bash
# Now that all required Python packages are installed, run the Flask app to make it visible across the network
flask run --host=0.0.0.0
```