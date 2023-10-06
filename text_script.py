from twilio.rest import Client

# Your Twilio Account SID and Auth Token
account_sid = 'ACb7d05057e45fec9473232fd0ae745f3d'
auth_token = '6474f7cb54b2bff78850503965ae5925'

# Create a Twilio client
client = Client(account_sid, auth_token)

# Your Twilio phone number (must be purchased from Twilio)
twilio_phone_number = '+12568277665'

# Recipient's phone number (passed as an argument)
def send_sms_notification(recipient_phone_number, message_body):
    try:
        # Send a text message
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=recipient_phone_number
        )
        
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")