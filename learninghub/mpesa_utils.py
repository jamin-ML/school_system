import requests
from requests.auth import HTTPBasicAuth

def get_mpesa_access_token():
    consumer_key = 'YbqFOpzWSRFnwkkvFbqM0Si4hf2eSHpZO2L1fy1chkFObaFD'
    consumer_secret = 'DRGgymb7IVmw8qSj0eeTermI92Z9EhRu83NxYvwk5drK7QzNmIWRYJMRywiYvFZ1'
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    response.raise_for_status()
    return response.json().get('access_token')

def register_mpesa_urls(confirmation_url, validation_url, shortcode='600000'):
    access_token = get_mpesa_access_token()
    register_url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
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
    response = requests.post(register_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json() 