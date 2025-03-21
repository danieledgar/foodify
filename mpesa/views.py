from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Transaction
from datetime import datetime
import json
from django.contrib import messages


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        try:
            
            data = json.loads(request.body)
            print("Received callback data:", data) 

            
            stk_callback = data.get('Body', {}).get('stkCallback', {})
            result_code = stk_callback.get('ResultCode', None)
            result_desc = stk_callback.get('ResultDesc', '')  
            transaction_id = stk_callback.get('CheckoutRequestID', None)

         
            if transaction_id:
                transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
                if transaction:
                    if result_code == 0:  
                        callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                        receipt_number = next((item.get('Value') for item in callback_metadata if item.get('Name') == 'MpesaReceiptNumber'), None)
                        amount = next((item.get('Value') for item in callback_metadata if item.get('Name') == 'Amount'), None)
                        transaction_date_str = next((item.get('Value') for item in callback_metadata if item.get('Name') == 'TransactionDate'), None)

                     
                        transaction_date = None
                        if transaction_date_str:
                            transaction_date = datetime.strptime(str(transaction_date_str), "%Y%m%d%H%M%S")

                   
                        transaction.mpesa_receipt_number = receipt_number
                        transaction.transaction_date = transaction_date
                        transaction.amount = amount
                        transaction.status = "Success"
                        transaction.description = "Payment successful"
                        transaction.save()

                        print(f"Transaction {transaction_id} updated as successful.")

                    elif result_code == 1:  
                        transaction.status = "Failed"
                        transaction.description = result_desc
                        transaction.save()
                        print(f"Transaction {transaction_id} marked as failed: {result_desc}")

                    elif result_code == 1032:  
                        transaction.status = "Cancelled"
                        transaction.description = "Transaction cancelled by the user"
                        transaction.save()
                        print(f"Transaction {transaction_id} marked as cancelled.")

            return JsonResponse({"message": "Callback received and processed"}, status=200)

        except Exception as e:
            print(f"Error processing callback: {e}")
            return JsonResponse({"error": "An error occurred while processing the callback"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def waiting_page(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    return render(request, 'mpesa/waiting.html', {'transaction_id': transaction_id})

def check_status(request, transaction_id):
    print(f"Checking status for transaction_id: {transaction_id}")  # Debugging
    transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
    print(f"Transaction status {transaction.status}")
    if not transaction:
        return JsonResponse({"status": "Failed", "message": "Transaction not found"}, status=404)

    if transaction.status == "Success":
        return JsonResponse({"status": "Success", "message": "Payment Successful"})
    elif transaction.status == "Failed":
        return JsonResponse({"status": "Failed", "message": "Payment Failed"})
    elif transaction.status == "Cancelled":
        return JsonResponse({"status": "Cancelled", "message": "Transaction was cancelled by the user"})
    else:
        return JsonResponse({"status": "Unknown", "message": "Transaction is still being processed or status is unknown"})

def payment_failed(request):
    messages.error(request,"Transaction failed")
    return redirect('order-summary')

def payment_cancelled(request):
    messages.error(request,"Transaction was cancelled")
    return redirect('order-summary')