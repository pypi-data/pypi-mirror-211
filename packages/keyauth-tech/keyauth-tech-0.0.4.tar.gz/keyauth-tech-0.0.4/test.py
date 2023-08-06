from keyauth import KeyAuth 

authenticator = KeyAuth(app_id="93b59d70ec573fa9")  # Replace with your actual app_id

if authenticator.authenticate():
    print("Authentication successful!")
else:
    print("Authentication failed.")
