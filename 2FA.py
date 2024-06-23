import pyotp
import time

# Dummy database for demonstration (replace with a real database in production)
users = {
    "user1": {
        "password": "password1",
        "otp_secret": "JBSWY3DPEHPK3PXP",  # TOTP secret (base32 encoded)
        "last_otp_timestamp": 0,  # Timestamp of last OTP generation
        "otp_validity": 30  # OTP validity in seconds
    }
}

def login(username, password):
    """Authenticate the user based on username and password."""
    if username in users and users[username]['password'] == password:
        return True
    else:
        return False

def generate_otp(username):
    """Generate a new OTP for the user."""
    if username in users:
        otp_secret = users[username]['otp_secret']
        totp = pyotp.TOTP(otp_secret)
        current_time = int(time.time())
        users[username]['last_otp_timestamp'] = current_time
        return totp.now()
    return None

def verify_otp(username, otp):
    """Verify the OTP entered by the user."""
    if username in users:
        otp_secret = users[username]['otp_secret']
        totp = pyotp.TOTP(otp_secret)
        if totp.verify(otp):
            current_time = int(time.time())
            last_otp_timestamp = users[username]['last_otp_timestamp']
            otp_validity = users[username]['otp_validity']
            if current_time - last_otp_timestamp <= otp_validity:
                return True
    return False

def main():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if login(username, password):
        otp = generate_otp(username)
        if otp:
            print(f"Generated OTP: {otp}")
            time.sleep(5)  # Simulate some delay before OTP verification
            entered_otp = input("Enter OTP from your authenticator app: ")
            if verify_otp(username, entered_otp):
                print(f"Welcome, {username}! OTP verification successful.")
            else:
                print("Invalid OTP or OTP expired. Access denied.")
        else:
            print("Failed to generate OTP. Access denied.")
    else:
        print("Invalid username or password. Access denied.")

if __name__ == "__main__":
    main()
