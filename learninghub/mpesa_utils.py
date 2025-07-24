# Import requests library for making HTTP requests
import requests
# Import HTTPBasicAuth for basic authentication with requests
from requests.auth import HTTPBasicAuth

# Function to get an access token from the M-Pesa API
def get_mpesa_access_token():
    consumer_key = 'YbqFOpzWSRFnwkkvFbqM0Si4hf2eSHpZO2L1fy1chkFObaFD'  # Sandbox consumer key
    consumer_secret = 'DRGgymb7IVmw8qSj0eeTermI92Z9EhRu83NxYvwk5drK7QzNmIWRYJMRywiYvFZ1'  # Sandbox consumer secret
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'  # Token endpoint
    # Make a GET request with basic auth to obtain the access token
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    response.raise_for_status()  # Raise an error if the request failed
    # Return the access token from the response JSON
    return response.json().get('access_token')

# Function to register confirmation and validation URLs with the M-Pesa API
# These URLs are called by M-Pesa when a payment event occurs
# confirmation_url: URL to receive payment confirmations
# validation_url: URL to receive payment validation requests
# shortcode: M-Pesa shortcode (default is sandbox value)
def register_mpesa_urls(confirmation_url, validation_url, shortcode='600000'):
    access_token = get_mpesa_access_token()  # Get the access token
    register_url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'  # Registration endpoint
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "ShortCode": shortcode,
        "ResponseType": "Completed",
        "ConfirmationURL": confirmation_url,
        "ValidationURL": validation_url
    }
    # Make a POST request to register the URLs
    response = requests.post(register_url, headers=headers, json=data)
    response.raise_for_status()  # Raise an error if the request failed
    # Return the response JSON
    return response.json() 