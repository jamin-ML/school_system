# Import decorator to exempt views from CSRF verification (for external API callbacks)
from django.views.decorators.csrf import csrf_exempt
# Import JsonResponse for returning JSON responses
from django.http import JsonResponse
# Import json module for parsing request bodies
import json
# Import models used in payment processing
from .models import Material, User

# View to handle M-Pesa payment confirmation callbacks
@csrf_exempt
def mpesa_confirmation(request):
    if request.method == 'POST':
        # Parse the JSON payload from M-Pesa
        data = json.loads(request.body)
        # Extract payment details from M-Pesa payload
        phone = data.get('MSISDN')
        amount = data.get('TransAmount')
        account = data.get('BillRefNumber')  # Use this as resource ID
        # Find the user and resource
        try:
            resource = Material.objects.get(id=account)#type: ignore
            # You may need to map phone to user, or require login before payment
            # For demo, just mark all as paid for this resource
            ResourcePayment.objects.filter(resource=resource).update(paid=True)#type: ignore
        except Material.DoesNotExist:#type: ignore
            pass
        # Respond to M-Pesa with success
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    # If not POST, reject the request
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Rejected"})

# View to handle M-Pesa payment validation callbacks
@csrf_exempt
def mpesa_validation(request):
    # For most cases, just accept all validation requests
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
