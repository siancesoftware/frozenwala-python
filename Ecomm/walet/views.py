from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from ecomApp.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import PurchaseBenefit

# Create your views here.
class WalletAPIView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.GET.get('user_id')

        if not user_id:
            return JsonResponse({'error': 'User ID parameter is missing'}, status=400)

        try:
            wallet_instance = Walet.objects.get(user_id=user_id)

            wallet_value = wallet_instance.wallet_value
            return JsonResponse({'wallet_value': wallet_value})
        except Walet.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ecomApp.models import CustomUser
from .models import Walet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

class UpdateWallet(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        user_id = request.data.get('user_id')
        cart_price = request.data.get('cart_price')

        # Check if user exists
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create wallet for the user
        wallet, created = Walet.objects.get_or_create(user_id=user.id)

        # Get amount to add to the wallet (user.walet or 0 if not provided)
        amount_to_add = int(user.walet)  # Assuming user.walet is a number

        # Ensure amount_to_add does not exceed cart_price
        #new
        if amount_to_add > int(cart_price):
            amount_to_add = int(cart_price) - 1


            
        if  wallet.wallet_value == amount_to_add:
            pass
        else:
            wallet.wallet_value += amount_to_add
            wallet.save()


        # Add amount to the wallet
        # wallet.wallet_value += amount_to_add
        # wallet.save()
        user = CustomUser.objects.get(id=user_id)
        #new
        # user.walet -= amount_to_add
        # user.save()
        return Response({"success": "Wallet updated successfully."}, status=status.HTTP_200_OK)
from decimal import Decimal
from decimal import Decimal

# def calculate_purchase_benefit(user_id, total_amount):
#     max_benefit_percentage = Decimal('0')
#     wallet_value = Decimal('0')
#
#     # Fetch purchase benefits and iterate through them
#     purchase_benefits = PurchaseBenefit.objects.filter(status='1')
#
#     for benefit in purchase_benefits:
#         if total_amount >= Decimal(benefit.price) and benefit.benefit_percentage > max_benefit_percentage:
#             max_benefit_percentage = Decimal(benefit.benefit_percentage)
#             wallet_value =  Decimal(total_amount) * (max_benefit_percentage / Decimal('100'))
#
#     # Convert wallet_value to int if necessary
#     wallet_value = int(wallet_value)
#
#     # Update wallet model amount
#     try:
#         wallet = Walet.objects.get(user_id=user_id)
#         wallet.wallet_value += wallet_value
#         wallet.save()
#     except Walet.DoesNotExist:
#         Walet.objects.create(user_id=user_id, wallet_value=wallet_value)
#
#     return max_benefit_percentage, wallet_value

def calculate_purchase_benefit(user_id, total_amount):
    max_benefit_percentage = Decimal('0')
    wallet_value = Decimal('0')

    # Fetch purchase benefits and iterate through them
    purchase_benefits = PurchaseBenefit.objects.filter(status='1')

    for benefit in purchase_benefits:
        if total_amount >= Decimal(benefit.price) and benefit.benefit_percentage > max_benefit_percentage:
            max_benefit_percentage = Decimal(benefit.benefit_percentage)
            wallet_value = Decimal(total_amount) * (max_benefit_percentage / Decimal('100'))

    # Convert wallet_value to int if necessary
    wallet_value = int(wallet_value)

    # Update CustomUser's wallet_value
    try:
        user = CustomUser.objects.get(id=user_id)
        wal=int(user.walet)
        wal += wallet_value  # ✔ Convert float to Decimal safely
        user.walet =wal
        user.save()
        # user.walet += wallet_value
        # user.save()
    except CustomUser.DoesNotExist:
        CustomUser.objects.create(id=user_id, wallet_value=wallet_value)

    return max_benefit_percentage, wallet_value
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PurchaseBenefit

@login_required(login_url='backend/login')
def purchase_benefit_list(request):
    if not request.user.is_staff:
        return redirect('backend/login')
    benefits = PurchaseBenefit.objects.all()
    context = {
        'benefits': benefits
    }
    return render(request, 'backend/purchase_benefit_list.html', context)

@login_required(login_url='backend/login')
def add_purchase_benefit(request):
    if not request.user.is_staff:
        return redirect('backend/login')
    if request.method == "POST":
        price = request.POST.get('price')
        benefit_percentage = request.POST.get('benefit_percentage')
        status = '1'  # Set status to '1' by default

        # Create the purchase benefit object
        PurchaseBenefit.objects.create(
            price=price,
            benefit_percentage=benefit_percentage,
            status=status
        )
        return redirect('purchase_benefit_list')

    return render(request, 'backend/add_purchase_benefit.html')

@login_required(login_url='backend/login')
def activate_purchase_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    benefit = get_object_or_404(PurchaseBenefit, id=benefit_id)
    benefit.status = '1'
    benefit.save()
    return redirect('purchase_benefit_list')

@login_required(login_url='backend/login')
def deactivate_purchase_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    benefit = get_object_or_404(PurchaseBenefit, id=benefit_id)
    benefit.status = '0'
    benefit.save()
    return redirect('purchase_benefit_list')

@login_required(login_url='backend/login')
def delete_purchase_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    benefit = get_object_or_404(PurchaseBenefit, id=benefit_id)
    benefit.delete()
    return redirect('purchase_benefit_list')

@login_required(login_url='backend/login')
def view_purchase_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    benefit = get_object_or_404(PurchaseBenefit, id=benefit_id)
    return render(request, 'backend/view_purchase_benefit.html', {'item': benefit})

@login_required(login_url='backend/login')
def update_purchase_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    benefit = get_object_or_404(PurchaseBenefit, id=benefit_id)

    if request.method == "POST":
        benefit.price = request.POST.get('price')
        benefit.benefit_percentage = request.POST.get('benefit_percentage')
        benefit.status = request.POST.get('status', '1')  # Set status to '1' by default if not provided
        benefit.save()
        return redirect('purchase_benefit_list')

    return render(request, 'backend/edit_purchase_benefit.html', {'item': benefit})

@login_required(login_url='backend/login')
def edit_purchase_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    benefit = get_object_or_404(PurchaseBenefit, id=benefit_id)
    all_benefits = PurchaseBenefit.objects.all()

    context = {
        'all_benefits': all_benefits,
        'benefit': benefit,
    }
    return render(request, 'backend/edit_purchase_benefit.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import InstallationBenefit

@login_required(login_url='backend/login')
def installation_benefit_list(request):
    if not request.user.is_staff:
        return redirect('backend/login')
    items = InstallationBenefit.objects.all()
    context = {
        'items': items
    }
    return render(request, 'backend/installation_benefit_list.html', context)

@login_required(login_url='backend/login')
def add_installation_benefit(request):
    if not request.user.is_staff:
        return redirect('backend/login')
    if request.method == "POST":
        price = request.POST.get('price')
        status = '1'

        InstallationBenefit.objects.create(
            price=price,
            status=status
        )
        return redirect('installation_benefit_list')

    return render(request, 'backend/add_installation_benefit.html')

@login_required(login_url='backend/login')
def activate_installation_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    item = get_object_or_404(InstallationBenefit, id=benefit_id)
    item.status = '1'
    item.save()
    return redirect('installation_benefit_list')

@login_required(login_url='backend/login')
def deactivate_installation_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    item = get_object_or_404(InstallationBenefit, id=benefit_id)
    item.status = '0'
    item.save()
    return redirect('installation_benefit_list')

@login_required(login_url='backend/login')
def delete_installation_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    item = get_object_or_404(InstallationBenefit, id=benefit_id)
    item.delete()
    return redirect('installation_benefit_list')

@login_required(login_url='backend/login')
def view_installation_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    item = get_object_or_404(InstallationBenefit, id=benefit_id)
    return render(request, 'backend/view_installation_benefit.html', {'item': item})

@login_required(login_url='backend/login')
def update_installation_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    edit_item = get_object_or_404(InstallationBenefit, id=benefit_id)

    if request.method == "POST":
        edit_item.price = request.POST.get('price')
        edit_item.save()
        return redirect('installation_benefit_list')

    return render(request, 'backend/edit_installation_benefit.html', {'sel_proform': edit_item})






from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ReferralBenefit

@login_required(login_url='backend/login')
def referral_benefit_list(request):
    if not request.user.is_staff:
        return redirect('backend/login')
    items = ReferralBenefit.objects.all()
    context = {
        'items': items
    }
    return render(request, 'backend/referral_benefit_list.html', context)

@login_required(login_url='backend/login')
def add_referral_benefit(request):
    if not request.user.is_staff:
        return redirect('backend/login')
    if request.method == "POST":
        price = request.POST.get('price')
        status = '1'

        ReferralBenefit.objects.create(
            price=price,
            status=status
        )
        return redirect('referral_benefit_list')

    return render(request, 'backend/add_referral_benefit.html')

@login_required(login_url='backend/login')
def activate_referral_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    item = get_object_or_404(ReferralBenefit, id=benefit_id)
    item.status = '1'
    item.save()
    return redirect('referral_benefit_list')

@login_required(login_url='backend/login')
def deactivate_referral_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    item = get_object_or_404(ReferralBenefit, id=benefit_id)
    item.status = '0'
    item.save()
    return redirect('referral_benefit_list')

@login_required(login_url='backend/login')
def delete_referral_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    item = get_object_or_404(ReferralBenefit, id=benefit_id)
    item.delete()
    return redirect('referral_benefit_list')

@login_required(login_url='backend/login')
def view_referral_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    item = get_object_or_404(ReferralBenefit, id=benefit_id)
    return render(request, 'backend/view_referral_benefit.html', {'item': item})

@login_required(login_url='backend/login')
def update_referral_benefit(request, benefit_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    edit_item = get_object_or_404(ReferralBenefit, id=benefit_id)

    if request.method == "POST":
        edit_item.price = request.POST.get('price')
        edit_item.save()
        return redirect('referral_benefit_list')

    return render(request, 'backend/edit_referral_benefit.html', {'sel_proform': edit_item})


# class RemoveWallet(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def delete(self, request):
#         user_id = request.query_params.get('user_id')
#
#         if not user_id:
#             return Response({"error": "User ID parameter is required"}, status=400)
#
#         # Check if user exists
#         try:
#             user = CustomUser.objects.get(id=user_id)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User does not exist."}, status=404)
#
#         # Check if wallet exists for the user
#         try:
#             wallet = Walet.objects.get(user_id=user.id)
#             wallet_value = wallet.wallet_value  # Get the wallet value before deleting
#
#             # Delete the wallet
#             wallet.delete()
#
#             # Add wallet value back to CustomUser's walet
#             #new
#             # user.walet += wallet_value
#             #user.save()
#
#             return Response({"success": "Wallet deleted successfully and amount added back to user's wallet."},
#                             status=200)
#
#         except Walet.DoesNotExist:
#             return Response({"error": "Wallet does not exist for the user."}, status=
class RemoveWallet(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_id = request.query_params.get('user_id')

        # Check if the user_id is provided
        if not user_id:
            return Response({"error": "User ID parameter is required"}, status=400)

        # Check if user exists, if not, return a neutral success response
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"success": "User does not exist or wallet could not be found."}, status=200)

        # Check if wallet exists for the user, if not, return a neutral success response
        try:
            wallet = Walet.objects.get(user_id=user.id)
            wallet_value = wallet.wallet_value  # Get the wallet value before deleting

            # Delete the wallet
            wallet.delete()

            # Add wallet value back to CustomUser's wallet (if the user has a wallet field)
            # user.wallet += wallet_value
            # user.save()

            return Response({
                "success": "Wallet deleted successfully and amount added back to user's wallet."
            }, status=200)

        except Walet.DoesNotExist:
            # If no wallet is found for the user, just return a neutral success message
            return Response({"success": "Wallet does not exist for the user."}, status=200)
