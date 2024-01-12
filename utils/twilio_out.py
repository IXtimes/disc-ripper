from preferences import load_preferences
from twilio.rest import Client
from typing import List

def post_to_numbers(msg, numbers: List[str] ):
    # Read the preferences file to get the Twilio client information
    preferences = load_preferences.load_preferences()
    account_sid = preferences[4]
    auth_token = preferences[5]
    bot_number = preferences[6]
    
    # Contact the Twillo client
    client = Client(account_sid, auth_token)
    
    # Iterate through the numbers
    for recipient in numbers:
        # Contact each number with the specified message
        message = client.messages.create(
                from_=bot_number,
                body=msg,
                to=recipient
        )
    
