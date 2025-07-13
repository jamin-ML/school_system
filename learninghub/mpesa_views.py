from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Resource, User, ResourcePayment

@csrf_exempt
def mpesa_confirmation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Extract payment details from M-Pesa payload
        phone = data.get('MSISDN')
        amount = data.get('TransAmount')
        account = data.get('BillRefNumber')  # Use this as resource ID
        # Find the user and resource
        try:
            resource = Resource.objects.get(id=account)#type: ignore
            # You may need to map phone to user, or require login before payment
            # For demo, just mark all as paid for this resource
            ResourcePayment.objects.filter(resource=resource).update(paid=True)#type: ignore
        except Resource.DoesNotExist:#type: ignore
            pass
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Rejected"})

@csrf_exempt
def mpesa_validation(request):
    # For most cases, just accept all
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
