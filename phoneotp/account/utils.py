from twilio.rest import Client

def send_otp_sms(self, phone_number, otp):
    # Twilio credentials
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Your OTP for registration: {otp}',
        from_='',
        to=phone_number
    )