from twilio.rest import Client

# Recipient's phone number (passed as an argument)
def send_sms_notification(recipient_phone_number, message_body, a_s, a_t):

    # Your Twilio Account SID and Auth Token
    account_sid = a_s
    auth_token = a_t

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Your Twilio phone number (must be purchased from Twilio)
    twilio_phone_number = '+12568277665'

    try:
        # Send a text message
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=recipient_phone_number
        )
        
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")