from django.db.models import Q
from django.shortcuts import render, redirect
from cart.models import CartCoupon
from pytz import timezone
import pytz
from datetime import datetime
# Create your views here.
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import  Order
from .serializers import OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ecomApp.models import CustomUser
from ecomApp.models import Catagory
from ecomApp.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from walet.models import PurchaseBenefit

#for noww...
class OrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import pytz
from django.utils import timezone

@login_required(login_url='backend/login')
def orderlist(request):
    if not request.user.is_staff:
        return redirect('backend/login')
    # Fetch all orders
    orders = Order.objects.all().order_by('-created_at')

    # Create a dictionary to store orders grouped by their order_id
    orders_dict = {}
    local_tz = pytz.timezone('Asia/Kolkata')
    for order in orders_dict.values():
        order.created_at = order.created_at.astimezone(local_tz)

    # Iterate over orders and group them by their order_id
    for order in orders:
        if order.payment_id:
            if order.order_id not in orders_dict:
                orders_dict[order.order_id] = order
    # Extract the first element of each group
    first_elements = [order for order in orders_dict.values()][:10]
    sec_elements = [order for order in orders_dict.values()]

    # Pass the first elements to the template context
    context = {
        'ordform': first_elements,
        'new': sec_elements
    }

    return render(request, 'backend/orderlist.html', context)
@login_required(login_url='backend/login')
def confirmorderlist(request):
    if not request.user.is_staff:
        return redirect('backend/login')
    ordercon=Order.objects.filter(Q(status=2) | Q(status=3) | Q(status=4))
    context={
        'ordercon':ordercon

    }
    return render(request,'backend/confirmorderlist.html',context)
@login_required(login_url='backend/login')
def view_item(request, myid):

     sel_ordform = Order.objects.filter(order_id=myid)
     ord = Order.objects.all()
     print(sel_ordform)
     if not request.user.is_staff:
         return redirect('backend/login')
     # related_orders = Order.objects.filter(order_id=sel_ordform.order_id)
     context = {
         'ordform': ord,
         'sel_ordform': sel_ordform
    }
     return render(request, 'backend/orderview.html', context)

@login_required(login_url='backend/login')
def suspend_user(request, catagory_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    order = get_object_or_404(Order, id=catagory_id)
    order.status = 2  # Change status to "confirm"
    order.save()
    return redirect('orderapp:activate_catagory', catagory_id=catagory_id)
@login_required(login_url='backend/login')
def cancel(request, catagory_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    order = get_object_or_404(Order, id=catagory_id)
    order.status = 5  # Change status to "cancel"
    order.save()
    return redirect('orderapp:returnrequest', catagory_id=catagory_id)
@login_required(login_url='backend/login')
def activate_catagory(request, catagory_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    order = get_object_or_404(Order, id=catagory_id)
    order.status = 3  # Change status to "pickup"
    order.save()
    return redirect('orderapp:deactivate_catagory', catagory_id=catagory_id)
@login_required(login_url='backend/login')
def deactivate_catagory(request, catagory_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    order = get_object_or_404(Order, id=catagory_id)
    order.status = 4  # Change status to "delivered"
    order.save()
    return redirect('orderapp:deliver', catagory_id=catagory_id)
@login_required(login_url='backend/login')
def deliver(request, catagory_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    order = get_object_or_404(Order, id=catagory_id)
    order.status = 4  # Change status to "delivered"
    order.save()
    return redirect('orderapp:index')  # Redirect to main page after delivery
@login_required(login_url='backend/login')
def returnrequest(request, catagory_id):
    if not request.user.is_staff:
        return redirect('backend/login')

    order = get_object_or_404(Order, id=catagory_id)
    order.status = 6  # Change status to "return request"
    order.save()
    return redirect('orderapp/returnaccepted', catagory_id=catagory_id)
@login_required(login_url='backend/login')
def returnaccepted(request, catagory_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    order = get_object_or_404(Order, id=catagory_id)
    order.status = 7  # Change status to "return accepted"
    order.save()
    return redirect('orderapp')  # Redi
# def returnrequest(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 6
#     banner.save()
#     return redirect('returnaccepted', catagory_id=catagory_id)
#
# def returnaccepted(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 7
#     banner.save()
#     return redirect('orderapp')  # Redirect to your category list view
#




from walet.views import calculate_purchase_benefit  # Adjust the import path as per your application structure





from walet.models import Walet
from ecomApp.models import Stock
import random
import string
from cart.models import Cart
def generate_random_order_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import secrets

from django.contrib import messages
import razorpay
from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from notification.views import SendNotificationAPI  # Import the SendNotificationAPI class

from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import json
import requests
from django.forms.models import model_to_dict
from django.contrib import messages
import requests
import json

def update_status(request, id):

    if not request.user.is_staff:
        return redirect('backend/login')

    if request.method == 'POST':
        selected_status_str = request.POST.get('selected_status')

        try:
            selected_status = int(selected_status_str)
        except (TypeError, ValueError):
            messages.error(request, 'Invalid status value!')
            return redirect('orderapp')

        order = Order.objects.get(id=id)
        order_id = order.order_id
        orders_to_update = Order.objects.filter(order_id=order_id)

        for order_obj in orders_to_update:
            order_obj.status = selected_status
            order_obj.save()

            if selected_status == 2:
                try:
                    stock = Stock.objects.get(item_id=order_obj.product_id)
                    openingStock  = stock.openingstock
                    stock.openingstock -= order_obj.quantity
                    stock.save()

                    # If stock is depleted, remove from cart
                    if stock.openingstock <= 0:
                        Cart.objects.filter(product_id=order_obj.product_id).delete()

                    # Notify external API with correct item_id field
                    try:
                        order_data = {
                            "item_id_id": order_obj.product_id.id,
                            "openingstock": openingStock - order_obj.quantity,
                            "piece_count": order_obj.quantity
                        }

                        headers = {'Content-Type': 'application/json'}
                        response = requests.post(
                            'https://bill.megasgoods.com/api/decrement-stock',
                            data=json.dumps(order_data),
                            headers=headers
                        )

                        if response.status_code != 200:
                            print("Failed to notify external API. Status code:", response.status_code)
                            print("Response:", response.text)
                        else:
                            print("External API notified successfully.")

                    except Exception as api_exc:
                        print("API notification failed:", str(api_exc))

                except Stock.DoesNotExist:
                    print(f"Stock not found for item_id {order_obj.product_id.id}")

        # Send notifications to the user
        if selected_status != 1:
            user = CustomUser.objects.get(id=order.user_id.id)
            registration_id = user.registration_id or 0

            notifications = {
                2: ("Order Confirmed", "Your order has been confirmed."),
                3: ("Order Picked Up", "Congrats! Your order has been picked up from FrozenWala Store Ruby Tower Jogeswari West, Mumbai, Maharashtra, India, 400102."),
                4: ("Order Delivered", "Your order has been delivered successfully."),
                5: ("Order Canceled", "Sorry! Your order has been canceled due to some internal reason."),
                7: ("Return Request Accepted", "Your return request has been accepted by the store.")
            }

            if selected_status in notifications:
                title, message = notifications[selected_status]
                SendNotificationAPI().send_notification(registration_id, title, message)

        messages.success(request, 'Status updated successfully!')

    return redirect('orderapp')

# def update_status(request, id):
#     if not request.user.is_staff:
#         return redirect('backend/login')
#     if request.method == 'POST':
#         selected_status_str = request.POST.get('selected_status')
#         try:
#             selected_status = int(selected_status_str)
#         except (TypeError, ValueError):
#             # Handle the case where selected_status_str is not a valid integer
#             messages.error(request, 'Invalid status value!')
#             # return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))
#             return redirect('orderapp')  # Redirect to order list page on error
# 
#         order = Order.objects.get(id=id)
# 
#         # Update status for each order
#         order_id = order.order_id
# 
#         # Retrieve all orders with the same order_id
#         orders_to_update = Order.objects.filter(order_id=order_id)
# 
#         # Update status for each order
#         for order_id in orders_to_update:
#             order_id.status = selected_status
#             order_id.save()
#             if selected_status == 2:
#                 try:
#                     stock = Stock.objects.get(item_id=order_id.product_id)
#                     stock.openingstock -= order_id.quantity
#                     stock.save()
# 
#                     # ✅ Remove from cart if stock is 0 or less
#                     if stock.openingstock <= 0:
#                         Cart.objects.filter(product_id=order_id.product_id).delete()
#                 except Stock.DoesNotExist:
#                     # You may want to log this or handle missing stock
#                     pass
#                 try:
#                     # Get the necessary order data, just the item_id in this case
#                     order_data = {
#                         'item_id_id': order_obj.item_id  # Assuming 'item_id' is the field in your order object
#                     }
# 
#                     # Optional: Add related user fields (you may still need user details)
#                     # order_data['username'] = order_obj.user_id.username
#                     # order_data['mobile'] = order_obj.user_id.cus_mobile
#                     #
#                     # # Optional: Add readable status
#                     # order_data['status_label'] = 'Confirmed'
# 
#                     # Only include the item_id in the API request
#                     headers = {'Content-Type': 'application/json'}
#                     response = requests.post(
#                         'https://bill.megasgoods.com/api/decrement-stock',
#                         data=json.dumps(order_data),  # Send only the item_id field
#                         headers=headers
#                     )
# 
#                     if response.status_code != 200:
#                         # Log failure
#                         print("Failed to notify external API")
#                 except Exception as e:
#                     print("API notification failed:", str(e))
# 
#         # Send notification to the user if the status has changed
#         if selected_status != 1:
#             uid=CustomUser.objects.get(id=order.user_id.id)
#             registration_id = uid.registration_id if uid.registration_id else 0
#             if selected_status == 2:
# 
#                 title = "Order Confirmed"
#                 message = "Your order has been confirmed."
#                 SendNotificationAPI().send_notification(registration_id, title, message)
# 
#             elif selected_status == 3:
#                 title = "Order Picked Up"
#                 message = "Congrats! Your order has been picked up from FrozenWala Store Ruby Tower Jogeswari West, Mumbai, Maharashtra, India, 400102."
#                 SendNotificationAPI().send_notification(registration_id, title, message)
# 
#             elif selected_status == 4:
#                 title = "Order Delivered"
#                 message = "Your order has been delivered successfully."
#                 SendNotificationAPI().send_notification(registration_id, title, message)
# 
#             elif selected_status == 5:
#                 title = "Order Canceled"
#                 message = "Sorry! Your order has been canceled due to some internal reason."
#                 SendNotificationAPI().send_notification(registration_id, title, message)
# 
#             elif selected_status == 7:
#                 title = "Return Request Accepted"
#                 message = "Your return request has been accepted by the store."
#                 SendNotificationAPI().send_notification(registration_id, title, message)
# 
#         messages.success(request, 'Status updated successfully!')
# 
#     return redirect('orderapp')  # Redirect to order list page on error


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET_KEY))

@csrf_exempt
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_order(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        total_amount = request.data.get('total_amount')
        dicounted_price = request.data.get('discounted_price', "")
        previous_price = request.data.get('previous_price')
        delivery_price = request.data.get('delivery_price', "")
        walet_value = request.data.get('walet_value',0)
        pick_up=request.data.get('pick_up')
        coupon_code = request.data.get('coupon_code', "")
        coupon_value = request.data.get('coupon_value')
        newname = request.data.get('newname', "")
        phone = request.data.get('phone', "")
        address = request.data.get('address', "Pick UP")
        city = request.data.get('city', "")
        state = request.data.get('state', "")
        country = request.data.get('country', "")
        zip_code = request.data.get('zip_code', "")
        delivery_time = request.data.get('delivery_time', ""),
        influencer_code = request.data.get('influencer_code', "")
        user = get_object_or_404(CustomUser, id=user_id)
        if not influencer_code:
            influencer_code = user.influencer_code if hasattr(user, 'influencer_code') else ""

        try:
            print(user_id)
            # Create order in Razorpay
            order_amount = int(float(total_amount) * 100)  # Amount in paisa
            order_currency = 'INR'
            order_receipt = 'order_receipt_' + str(user_id)  # You can set it as per your requirement
            razorpay_order = razorpay_client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt))

            # Get cart items for the user
            cart_items = Cart.objects.filter(u_id=user_id, status='Active')
            # max_benefit_percentage, wallet_value = calculate_purchase_benefit(user_id, total_amount)

            #new
            for cart_item in cart_items:
                # Get the stock for the item
                stock = get_object_or_404(Stock, item_id=cart_item.product_id)

                # Check if the stock is sufficient
                if stock.openingstock < cart_item.quantity:
                    return JsonResponse({'message': f"Stock is not available for {cart_item.product_id.title}",'status':'400'},
                                        status=400)

            # Create orders for each item in the cart
            for cart_item in cart_items:
                Order.objects.create(
                    order_id=razorpay_order['id'],
                    user_id=CustomUser.objects.get(id=user_id),
                    product_id=cart_item.product_id,
                    payment_id='',  # Leave payment_id empty initially
                    couponcode=coupon_code,
                    walet_value=walet_value,
                    influencer_code=influencer_code,
                    # percentage_benefit=max_benefit_percentage,  # Save the percentage benefit
                    pick_up=pick_up,
                    status=1,  # Set initial status
                    quantity=cart_item.quantity,
                    price="{:.2f}".format(cart_item.price),
                    total_price=total_amount,
                    previous_price=previous_price,
                    dicounted_price=dicounted_price,
                    delivery_price=delivery_price,
                    signature='',  # Leave signature empty initially
                    newname=newname,
                    phone=phone,
                    address=address,
                    city=city,
                    state=state,
                    country=country,
                    zip_code=zip_code,
                    delivery_time=delivery_time,

                )

            return JsonResponse({'razorpay_order_id': razorpay_order['id'], 'couponcode': coupon_code, 'total_price': total_amount,'status':'success'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseServerError("Method Not Allowed")
from uuid import uuid4  # Import UUID generator

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    if request.method == 'POST':
        try:
            razorpay_payment_id = request.data.get('razorpay_payment_id')
            razorpay_order_id = request.data.get('razorpay_order_id')
            razorpay_signature = request.data.get('razorpay_signature')

            # Verify payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)

            # Update order status or save payment details to your database
            orders = Order.objects.filter(order_id=razorpay_order_id)

            for order in orders:
                # Generate a unique order item ID
                order_item_id = str(uuid4())
                order.payment_id = razorpay_payment_id
                order.signature = razorpay_signature
                order.status = 1  # Set status to success
                order.order_item_id = order_item_id
                order.save()

                # stock = Stock.objects.select_for_update().filter(item_id=order.product_id).first()
                # stock.openingstock -= 1
                # stock.save()
                product_id = order.product_id
                quantity = order.quantity
                # stock = Stock.objects.select_for_update().get(item_id=product_id)
                stock = Stock.objects.get(item_id=product_id)

               #for stock new
               # stock.openingstock -= quantity
                stock.save()
                if stock.openingstock <= 0:
                    Cart.objects.filter(product_id=product_id).delete()

            first_order = orders.first()
            user_id = first_order.user_id.id
            total_amount = first_order.total_price
            print(user_id, total_amount)
            max_benefit_percentage, wallet_value = calculate_purchase_benefit(user_id, total_amount)
            # Get the user_id from the first order

            cart_items = Cart.objects.filter(u_id=user_id, status='Active')
            cart_items.delete()
            cart_coupon = CartCoupon.objects.filter(user_id=user_id)
            if cart_coupon:
                cart_coupon.delete()
            cart_walet=Walet.objects.filter(user_id=user_id)
            if cart_walet:
                cart_walet.delete()
                
            #new
            if first_order.walet_value:
                user = CustomUser.objects.get(id=user_id)  # Fetch the user object based on user_id
                user_walet= int( user.walet)
                curr_wallet= int(first_order.walet_value)
                user_walet -= curr_wallet
                user.walet = user_walet

                user.save()

            alluser = CustomUser.objects.filter(id=user_id)
            userss = alluser.first()

            # Get the registration_id of the user
            registration_id = userss.registration_id
            title = "Order Placed Successfully!"
            message = "Your order has been successfully placed at FrozenwalaStore."
            SendNotificationAPI().send_notification(registration_id, title, message)



            return JsonResponse({'message': 'Payment successful'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        else:
            return HttpResponseServerError("Method Not Allowed")
from rest_framework import generics
from rest_framework.response import Response
from .models import Order
from .serializers import GroupedOrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from django.db.models import Max, Q

class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('user_id')

        # Fetch all orders for the given user where payment_id is not null
        orders = Order.objects.filter(user_id=user_id, payment_id__isnull=False)

        # Group orders by order_id, keeping the latest order with the highest created_at timestamp
        unique_orders = orders.values('order_id').annotate(
            latest_created_at=Max('created_at'),
            total_price=Max('total_price'),
            status=Max('status'),
            payment_id=Max('payment_id')
        )

        # Construct list of dictionaries for each unique order
        order_list = []
        local_tz = pytz.timezone('Asia/Kolkata')
        for order in unique_orders:
            if order['payment_id']:
                # Check if payment_id is not empty or null
                # Convert UTC to local timezone
                local_created_at = order['latest_created_at'].astimezone(local_tz)
                order_dict = {
                    'order_id': order['order_id'],
                    'created_at': local_created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'total_price': order['total_price'],
                    'status': order['status']
                }
                order_list.append(order_dict)

        # Sort the order list in descending order based on created_at
        sorted_order_list = sorted(order_list, key=lambda x: x['created_at'], reverse=True)

        return Response(sorted_order_list)

        return Response(sorted_order_list)
from datetime import date
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class OrderDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the order_id from query parameters
            order_id = request.query_params.get('order_id')

            # Check if order_id parameter is provided
            if order_id is None:
                return Response({"error": "order_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve all orders for the specified order_id
            orders = Order.objects.filter(order_id=order_id)

            # If no orders found for the given order_id
            if not orders:
                return Response({"error": "No orders found for the given order_id"}, status=status.HTTP_404_NOT_FOUND)

            # Initialize lists to store product details and order details
            products = []
            order_details = []

            # Iterate over orders
            for order in orders:
                # Retrieve product details for all orders
                product = {
                    "product_id": order.product_id.id,
                    "name": order.product_id.title,
                    "description": order.product_id.description,
                    # "item_photo": order.product_id.item_photo.url,
                    "item_quantity": order.quantity,
                    # "item_measurement": order.product_id.item_measurement,
                    "item_old_price": order.product_id.item_old_price,
                    "discount": order.product_id.discount,
                    "item_new_price": order.product_id.item_new_price,
                    "product_order_price":order.product_id.item_new_price*order.quantity,
                    "status": order.product_id.status,
                    "category": order.product_id.category.name,
                    "created_at": order.product_id.created_at,
                    "deal_of_the_day": order.product_id.deal_of_the_day,
                    "recommended": order.product_id.recommended,
                    "most_popular": order.product_id.most_popular
                }
                products.append(product)

                # Append full order details for the first order only
                if not order_details:  # Ensures only the first order details are added
                    order_detail = {
                        "order_id": order.order_id,
                        "status": order.status,
                        "total_price": order.total_price,
                        "discounted_price": order.dicounted_price,
                        "previous_price": order.previous_price,
                        "delivery_price":order.delivery_price,
                        "coupon_code":order.couponcode,
                        # "item_price": order.price,
                        # "created_at": order.created_at,
                        "newname": order.newname,
                        "phone": order.phone,
                        "address": order.address,
                        "city": order.city,
                        "state": order.state,
                        "country": order.country,
                        "zip_code": order.zip_code,
                        "delivery_time": order.delivery_time,
                        "wallet": order.walet_value,

                        # "order_item_id": order.order_item_id
                    }
                    order_details.append(order_detail)

            return Response({"order_details": order_details, "products": products}, status=status.HTTP_200_OK)



        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import JsonResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from pytz import timezone
import pytz
from .models import Order

from django.http import JsonResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from django.http import JsonResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import pytz
from pytz import timezone

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from django.http import HttpResponse
from django.utils.timezone import localtime
from pytz import timezone
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from pathlib import Path  # To handle paths in a cross-platform way

def generate_invoice(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        return JsonResponse({'error': 'Order ID is required'}, status=400)

    # Retrieve one order's items with the given order_id
    order_items = Order.objects.filter(order_id=order_id)
    local_tz = timezone('Asia/Kolkata')

    if not order_items:
        return JsonResponse({'error': 'No items found for the specified order ID'}, status=404)

    # Create PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order_id}.pdf'

    # Create a ReportLab PDF document
    doc = SimpleDocTemplate(response, pagesize=letter, topMargin=20)  # Adjust topMargin as needed
    styles = getSampleStyleSheet()

    # Customize styles
    styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Title'], fontSize=18))
    styles.add(ParagraphStyle(name='CustomNormal', parent=styles['Normal'], fontSize=12, leading=16))
    styles.add(ParagraphStyle(name='CustomHeading2', parent=styles['Heading2'], fontSize=14, leading=18))

    elements = []
    order = order_items.first()  # Assuming all items belong to the same order
    order.created_at = order.created_at.astimezone(local_tz)  # Convert to local timezone
    created_at_formatted = order.created_at.strftime('%d %B %Y, %I:%M %p')  # Format as "day Month Year, hh:mm AM/PM"
    elements.append(Spacer(1, 12))

    # Add logo
    logo_path = Path('ecomApp/static/assets/images/Frozenwala logo.png')  # Replace with the correct path
    if logo_path.exists():
        logo = Image(str(logo_path), width=150, height=150)  # Adjust width and height as needed
        elements.append(logo)
    else:
        elements.append(Paragraph('Logo not found', styles['CustomNormal']))

    elements.append(Spacer(1, 12))  # Spacer after the logo

    # Add title for the invoice
    elements.append(Paragraph('FROZENWALA ', styles['CustomTitle']))
    elements.append(Paragraph('ruby tower jogeshwari west, mumbai, Maharashtra - 400102', styles['CustomNormal']))
    elements.append(Paragraph(f'Order Placed On: {created_at_formatted}', styles['CustomNormal']))
    elements.append(Paragraph('Phone Number - 8268888826', styles['CustomNormal']))
    elements.append(Paragraph('GSTN - 27AKFPB3371A1ZS', styles['CustomNormal']))

    # Spacer before logo (adjust as needed)

    # Horizontal line
    elements.append(HRFlowable(width="100%", thickness=1, color='black'))
    elements.append(Spacer(1, 12))

    # Order and customer details
    elements.append(Paragraph(f'Customer Name - {order.newname}', styles['CustomNormal']))
    elements.append(Paragraph(f'Customer Number - {order.phone}', styles['CustomNormal']))
    elements.append(
        Paragraph(f'Address - {order.address}, {order.city}, {order.state}, {order.country}, {order.zip_code}',
                  styles['CustomNormal']))
    elements.append(Paragraph(f'Order Number - {order.order_id}', styles['CustomNormal']))
    elements.append(Spacer(1, 12))

    # Horizontal line
    elements.append(HRFlowable(width="100%", thickness=1, color='black'))
    elements.append(Spacer(1, 12))

    # Table headers
    data = [['Items', 'Qty.', 'Total(₹)']]
    elements.append(Spacer(1, 12))

    # Table data
    for item in order_items:
        item_title = item.product_id.title if item.product_id and item.product_id.title else 'N/A'
        item_quantity = item.quantity if item.quantity else 0
        item_total_price = float(item.product_id.item_new_price) if item.product_id.item_new_price else 0.0
        data.append([item_title, item_quantity, f'{item_total_price:.2f}'])

    # Create table
    table = Table(data, colWidths=[300, 50, 100])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, 'black')
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Horizontal line
    elements.append(HRFlowable(width="100%", thickness=1, color='black'))
    elements.append(Spacer(1, 12))

    # Order totals
    item_total = float(order.previous_price) if order.previous_price else 0.0
    delivery_price = float(order.delivery_price) if order.delivery_price else 0.0
    total_price = float(order.total_price) if order.total_price else 0.0

    elements.append(Paragraph(f'Item Total: {item_total:.2f}', styles['CustomNormal']))
    elements.append(Paragraph(f'Delivery Charge: {delivery_price:.2f}', styles['CustomNormal']))

    if order.couponcode:
        elements.append(Paragraph(f'Coupon Discount: {order.couponcode}', styles['CustomNormal']))
    else:
        elements.append(Paragraph('Applied Coupon: NA', styles['CustomNormal']))

    if order.walet_value:
        elements.append(Paragraph(f'Wallet Used: {order.walet_value}', styles['CustomNormal']))
    else:
        elements.append(Paragraph('Wallet Used: NA', styles['CustomNormal']))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f'Total Amount: {total_price:.2f}', styles['CustomHeading2']))

    # Horizontal line
    elements.append(HRFlowable(width="100%", thickness=1, color='black'))
    elements.append(Spacer(1, 12))

    # Center align elements
    for element in elements:
        element.alignment = 1  # 1 means center alignment

    # Build PDF
    doc.build(elements)
    return response