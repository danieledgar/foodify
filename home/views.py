from django.shortcuts import render, redirect, get_object_or_404
from hotel.models import Menu, Cart, CartItem, Order, OrderItem, Hotel
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from mpesa.credentials import MpesaAccessToken, MpesaPassword
from mpesa.models import Transaction


# Create your views here.
def home(request):
    hotel = Hotel.objects.all()
    
    context= {
        'hotels':hotel,
    }
    return render(request, 'home/home.html', context)

def menulist(request):
    menu_list = Menu.objects.all()

    context = {
        'menus':menu_list,
    }

    return render(request,'home/menu_list.html', context)

def hotels(request):
    hotels = Hotel.objects.all()

    context = {
        'hotels': hotels
    }

    return render(request, 'home/hotel_list.html',context)

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel,id = hotel_id)
    menulist = Menu.objects.filter(hotel = hotel_id)

    context = {
        'hotel': hotel,
        'menus': menulist
    }

    return render(request, 'home/hotel_detail.html',context)

def menu_detail(request, menu_id):
    menu_detail = get_object_or_404(Menu,id = menu_id)
    menulist = Menu.objects.filter(title = menu_detail.title).exclude(id = menu_id)

    context = {
        'menu_detail': menu_detail,
        'menus': menulist
    }

    return render(request, 'home/menu_detail.html',context)

# Get or create a cart for the user
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def add_to_cart(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)
    cart = get_user_cart(request.user)

    # Check if item already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{menu_item.title} added to cart.")
    return redirect('cart')

@login_required
def view_cart(request):
    cart = get_user_cart(request.user)

    context = {
        'cart': cart
    }
    return render(request, 'home/cart.html', context)

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully.")
        else:
            messages.error(request, "Quantity must be greater than zero.")
    return redirect('cart')

@login_required
def order(request):
    orders = Order.objects.filter(user = request.user).order_by('-created_at')

    context = {
        'orders': orders
    }

    return render(request,'home/order_list.html', context)


def order_summary(request):
    cart_ins = Cart.objects.get(user = request.user)
    # Retrieve the user's cart items
    menu_items = CartItem.objects.filter(cart=cart_ins.id)

    if not menu_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart')
    
    total_cost = cart_ins.total_price

    context = {
        'menu_items':menu_items,
        'total_cost': total_cost
    }
    if request.method == 'POST':
        phone = request.POST['phone']
        if not phone:
            messages.error(request, "Phone number is required!")
            return redirect('order-summary')
        payment_phone = validate_number(phone)
        amount = total_cost
        access_token = MpesaAccessToken.get_mpesa_access_token()
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {"Authorization": f"Bearer {access_token}"}

        transaction = Transaction.objects.create(
            phone_number=payment_phone,
            amount=amount(),
            status="Pending",
            description="Awaiting callback",
            name=request.user.username,
        )

        # Payload for Mpesa API
        payload = {
            "BusinessShortCode": MpesaPassword.get_business_short_code(),
            "Password": MpesaPassword.get_decoded_password(),
            "Timestamp": MpesaPassword.get_lipa_time(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount(),
            "PartyA": payment_phone,
            "PartyB": MpesaPassword.get_business_short_code(),
            "PhoneNumber": payment_phone,
            "CallBackURL": "https://lets-bite.onrender.com/mpesa/callback/",
            "AccountReference": "Lets_Bite",
            "TransactionDesc": "Payment for order",
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                messages.success(request, "Payment initiated successfully!")
                transaction_id = response_data.get('CheckoutRequestID', None)
                transaction.transaction_id = transaction_id
                transaction.description = response_data.get('ResponseDescription', 'No description')
                transaction.save()

                return redirect('waiting-page',transaction_id = transaction.transaction_id)
            else:
                error_message = response_data.get("errorMessage", "An error occurred.")
                messages.error(request, f"Payment failed: {error_message}")

        except requests.RequestException as e:
            messages.error(request, f"An error occurred while connecting to Mpesa: {str(e)}")

        
    return render(request,'home/order_summary.html', context)

@login_required
def checkout(request):
    cart_ins = Cart.objects.get(user = request.user)
    # Retrieve the user's cart items
    cart_items = CartItem.objects.filter(cart=cart_ins.id)
    item_instance = CartItem.objects.filter(cart = cart_ins.id).first()
    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    # Create an order
    order = Order.objects.create(user=request.user, cost= cart_ins.total_price(), hotel = item_instance.menu_item.hotel)
    
    # Add items to the order
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            menu_item=item.menu_item,
            quantity=item.quantity,
            price=item.menu_item.price
        )
    
    # Clear the cart
    cart_items.delete()

    messages.success(request, "Your order has been placed successfully!")
    return redirect('order-details', order_id=order.id)

def order_details(request,order_id):
    order = Order.objects.get(id= order_id)

    context = {
        'order':order
    }
    return render(request,'home/order-details.html', context)

def validate_number(input):
    # Ensure inputs are strings for easy manipulation
    input = str(input)
    prefix = str(254)
    
    # Get the last 9 digits
    trimmed = input[-9:]
    
    # Prepend the prefix
    result = prefix + trimmed
    
    return result
