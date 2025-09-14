from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer,CartGetSerializer
from ecomApp.models import CustomUser
from menu_management.models import Item
from rest_framework.permissions import IsAuthenticated
from walet.models import Walet
class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # old code
            product_id = request.data.get('product_id')
            u_id = request.data.get('u_id')
            try:
                wallet = Walet.objects.get(user_id=u_id)
                wallet_value = wallet.wallet_value  # Get the wallet value before deleting

                # Delete the wallet
                wallet.delete()

                # Add wallet value back to CustomUser's walet
                # new
                # user.walet += wallet_value
                # user.save()
                pass

                # return Response({"success": "Wallet deleted successfully and amount added back to user's wallet."},
                #                 status=200)

            except Walet.DoesNotExist:
                pass
            if product_id or u_id: 
                product = Item.objects.filter(id=product_id).first()
                if not product:
                    return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)
                user = CustomUser.objects.filter(id=u_id).first()
                if not user:
                    return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
                cart_items = Cart.objects.filter(product_id=product, u_id=user)
                if cart_items.exists():
                    cart_item = cart_items.first()
                    cart_item.quantity += 1
                    cart_item.price = cart_item.quantity * product.item_new_price
                else:
                    cart_item = Cart.objects.create(product_id=product, u_id=user, quantity=1,
                                                    price=product.item_new_price)
                cart_item.save()
                serializer = CartSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # new code
                cart = request.data.get('cart')
                user_id = request.data.get('user_id')
                user = CustomUser.objects.filter(id=user_id).first()
                if not user:
                    return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
                for product in cart:
                    item = Item.objects.filter(id=product['id']).first()
                    if item:
                        cart_item = Cart.objects.filter(product_id=item, u_id=user)
                        stock = Stock.objects.filter(item_id=item).first()
                        if cart_item and cart_item.quantity < stock.openingstock:
                            cart_item.quantity = cart_item.quantity + product['qty']
                            cart_item.price = item.item_new_price * cart_item.quantity
                            cart_item.save()
                        elif not cart_item:
                            if int(product['qty']) < stock.openingstock:
                                price = item.item_new_price * int(product['qty'])
                                quantity = product['qty']
                            else:
                                price = item.item_new_price
                                quantity = 1
                            Cart.objects.create(product_id=item, u_id=user, quantity=quantity, price=price)
                        else:
                            return Response({"error": "Out of stock"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'status': True}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class CartDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the user_id from query parameters
            user_id = request.query_params.get('user_id')

            # Validate user_id parameter
            if not user_id:
                return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve all cart items for the specified user_id
            cart_items = Cart.objects.filter(u_id=user_id)

            # Serialize the cart items
            serializer = CartSerializer(cart_items, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from ecomApp.models import Stock
class IncreaseQuantity(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart_id = request.data.get('cart_id')

            # Retrieve the cart item
            cart_item = Cart.objects.get(id=cart_id)
            try:
                wallet = Walet.objects.get(user_id=cart_item.u_id.id)
                wallet_value = wallet.wallet_value  # Get the wallet value before deleting

                # Delete the wallet
                wallet.delete()

                # Add wallet value back to CustomUser's walet
                # new
                # user.walet += wallet_value
                # user.save()
                pass

                # return Response({"success": "Wallet deleted successfully and amount added back to user's wallet."},
                #                 status=200)

            except Walet.DoesNotExist:
                pass
            stock=Stock.objects.get(item_id=cart_item.product_id)
            # Check if quantity is less than opening stock
            if cart_item.quantity < stock.openingstock:
                # Increment quantity
                cart_item.quantity += 1
                cart_item.save()

                # Update total price
                cart_item.price = cart_item.product_id.item_new_price * cart_item.quantity
                cart_item.save()

                return Response({"message": "Quantity increased successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Quantity cannot be increased beyond opening stock."},
                                status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# class DecreaseQuantity(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         try:
#             cart_id = request.data.get('cart_id')
#
#             # Retrieve the cart item
#             cart_item = Cart.objects.get(id=cart_id)
#
#             # Ensure quantity is greater than 1 before decrementing
#             if cart_item.quantity > 1:
#                 # Decrement quantity
#                 cart_item.quantity -= 1
#                 cart_item.save()
#
#                 # Update total price
#                 cart_item.price = cart_item.product_id.item_new_price * cart_item.quantity
#                 cart_item.save()
#
#                 return Response({"message": "Quantity decreased successfully."}, status=status.HTTP_200_OK)
#             else:
#                 cart_item.delete()
#                 return Response({"error": "Quantity cannot be less than 1."}, status=status.HTTP_400_BAD_REQUEST)
#         except Cart.DoesNotExist:
#             return Response({"error": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#new
class DecreaseQuantity(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart_id = request.data.get('cart_id')

            # Retrieve the cart item
            cart_item = Cart.objects.get(id=cart_id)
            try:
                wallet = Walet.objects.get(user_id=cart_item.u_id.id)
                wallet_value = wallet.wallet_value  # Get the wallet value before deleting

                # Delete the wallet
                wallet.delete()

                # Add wallet value back to CustomUser's walet
                # new
                # user.walet += wallet_value
                # user.save()
                pass

                # return Response({"success": "Wallet deleted successfully and amount added back to user's wallet."},
                #                 status=200)

            except Walet.DoesNotExist:
                pass
                # Ensure quantity is greater than 1 before decrementing
            if cart_item.quantity > 1:
                # Decrement quantity
                cart_item.quantity -= 1
                cart_item.save()

                # Update total price
                cart_item.price = cart_item.product_id.item_new_price * cart_item.quantity
                cart_item.save()

                return Response({"message": "Quantity decreased successfully."}, status=status.HTTP_200_OK)
            else:
                cart_item.delete()
                return Response({"error": "Quantity cannot be less than 1."}, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({"error": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class RemoveCartItem(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def delete(self, request):
#         try:
#             cart_id = request.query_params.get('cart_id')
#
#             # Check if cart_id parameter is provided and if it's a valid integer
#             if not cart_id.isdigit():
#                 return Response({"error": "Valid cart_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Retrieve the cart item
#             cart_item = Cart.objects.get(id=int(cart_id))
#
#             # Delete the cart item
#             cart_item.delete()
#
#             return Response({"message": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)
#         except Cart.DoesNotExist:
#             return Response({"error": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)
#         except ValueError:
#             return Response({"error": "Invalid cart_id provided."}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#new
class RemoveCartItem(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            cart_id = request.query_params.get('cart_id')
            cart_id=int(cart_id)

            # Check if cart_id parameter is provided and if it's a valid integer
            # if not cart_id.isdigit():
            #     return Response({"error": "Valid cart_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the cart item
            cart_item = Cart.objects.get(id=int(cart_id))
            # wallet = Walet.objects.get(user_id=cart_item.u_id.id)
            # # wallet_value = wallet.wallet_value  # Get the wallet value before deleting
            #
            # # Delete the wallet
            # wallet.delete()
            # wallet = Walet.objects.get(user_id=cart_item.u_id.id)
            try:
                wallet = Walet.objects.get(user_id=cart_item.u_id.id)
                # wallet_value = wallet.wallet_value  # Get the wallet value before deleting

                # Delete the wallet
                wallet.delete()

                # Add wallet value back to CustomUser's walet
                # new
                # user.walet += wallet_value
                # user.save()
                pass

                # return Response({"success": "Wallet deleted successfully and amount added back to user's wallet."},
                #                 status=200)

            except Walet.DoesNotExist:
                pass
            cart_item.delete()

            return Response({"message": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"error": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid cart_id provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# class CartTotalPrice(APIView):
#     def get(self, request):
#         try:
#             # Get the user_id from query parameters
#             user_id = request.query_params.get('user_id')
#
#             # Check if user_id parameter is provided
#             if user_id is None:
#                 return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Check if user_id is a valid integer
#             if not str(user_id).isdigit():
#                 return Response({"error": "Valid user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Retrieve all cart items for the specified user_id
#             cart_items = Cart.objects.filter(u_id=user_id)
#
#             # Calculate total price by summing the prices of all cart items
#             total_price = sum(cart_item.price for cart_item in cart_items)
#
#             return Response({"total_price": total_price}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from datetime import date
from django.utils import timezone
from ecomApp.models import CustomerCoupon,DeliveryCharge
from order.models import Order
from .models import CartCoupon
import math
from walet.models import Walet
import math

class CartTotalPrice(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            pick_up = request.query_params.get('pick_up')
            if pick_up == '1':
                delivery_charge = 0
            else:
                delivery_charge = DeliveryCharge.objects.first().charge

            user_id = request.query_params.get('user_id')

            if user_id is None:
                return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            if not str(user_id).isdigit():
                return Response({"error": "Valid user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            cart_items = Cart.objects.filter(u_id=user_id)
            total_price = sum(cart_item.price for cart_item in cart_items)
            previous_price = total_price
            discounted_price = 0
            today_date = date.today()

            try:
                coupon_value_param = CartCoupon.objects.get(user_id=user_id).coupon_code

                if coupon_value_param:
                    try:
                        coupon = CustomerCoupon.objects.get(
                            coupon=coupon_value_param,
                            start_date__lte=today_date,
                            expire_date__gte=today_date
                        )

                        discounted_price = total_price * (int(coupon.coupon_value) / 100)
                        total_price -= discounted_price
                    except CustomerCoupon.DoesNotExist:
                        pass
            except CartCoupon.DoesNotExist:
                pass
            wallet_value =0
            try:
                wallet = Walet.objects.get(user_id=user_id)
                wallet_value = float(wallet.wallet_value)
                total_price -= wallet_value
            except Walet.DoesNotExist:
                wallet_value = None

            if delivery_charge:
                total_price += delivery_charge

            total_price = math.ceil(total_price * 100) / 100
            previous_price = math.ceil(previous_price * 100) / 100
            discounted_price = math.ceil(discounted_price * 100) / 100
            if delivery_charge:
                delivery_charge = math.ceil(delivery_charge * 100) / 100
            rounded_total_price = math.ceil(total_price)
            current_wallet=0

            # current_wallet = CustomUser.objects.get(id=user_id).walet - wallet_value if wallet_value is not None else CustomUser.objects.get(id=user_id).walet
           #new
            # Retrieve the user's wallet balance from the CustomUser model
            user_wallet = CustomUser.objects.get(id=user_id).walet

            # Check if wallet_value is not None and not 0
            if wallet_value is not None:
                current_wallet = user_wallet - wallet_value  # Subtract wallet_value from the user's wallet
            else:
                current_wallet = user_wallet  # Keep the current wallet value if no wallet_value or wallet_value is 0

            return Response({
                "total_price": rounded_total_price,
                "previous_price": previous_price,
                "discounted_price": discounted_price,
                "delivery_charge": delivery_charge if delivery_charge else 0,
                "wallet_value": wallet_value or 0,
                "current_wallet": current_wallet
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from .models import CartCoupon
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_coupon(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        print("Received user_id:", user_id)  # Log the received user_id for debugging

        coupon = request.data.get('coupon')

        try:
            user = CustomUser.objects.get(id=user_id)
            try:
                existing_coupon = CartCoupon.objects.get(user_id=user.id)
                existing_coupon.coupon_code = coupon
                existing_coupon.save()
                message = 'Coupon updated successfully'
            except CartCoupon.DoesNotExist:
                coupon = CartCoupon.objects.create(user_id=user.id, coupon_code=coupon)
                message = 'Coupon sent successfully'
            return JsonResponse({'message': message})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



class IncreaseQuantityMain(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.data.get('product_id')
            user_id = request.data.get('user_id')
            
            user = CustomUser.objects.filter(id=user_id).first()
            if not user:
                return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Retrieve the cart item
            cart_item = Cart.objects.get(product_id=product_id, u_id=user_id)
            try:
                wallet = Walet.objects.get(user_id=cart_item.u_id.id)
                wallet_value = wallet.wallet_value  # Get the wallet value before deleting

                # Delete the wallet
                wallet.delete()

                # Add wallet value back to CustomUser's walet
                # new
                # user.walet += wallet_value
                # user.save()
                pass

                # return Response({"success": "Wallet deleted successfully and amount added back to user's wallet."},
                #                 status=200)

            except Walet.DoesNotExist:
                pass
            
            stock = Stock.objects.get(item_id=product_id)

            # Check if quantity is less than opening stock
            if cart_item.quantity < stock.openingstock:
                # Increment quantity
                cart_item.quantity += 1
                cart_item.save()

                # Update total price
                cart_item.price = cart_item.product_id.item_new_price * cart_item.quantity
                cart_item.save()

                cart_items = Cart.objects.filter(u_id=user_id)
                serializer = CartSerializer(cart_items, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Quantity cannot be increased beyond opening stock."},
                                status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            item = Item.objects.filter(id=product_id).first()
            Cart.objects.create(product_id=item, u_id=user, quantity=1, price=item.item_new_price)
            cart_items = Cart.objects.filter(u_id=user)
            serializer = CartSerializer(cart_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Stock.DoesNotExist:
            return Response({"error": "Stock information not available for the product."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# class DecreaseQuantityMain(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         try:
#             product_id = request.data.get('product_id')
#             user_id = request.data.get('user_id')
#
#             action = request.data.get('action')
#
#             if action == 'remove':
#                 Cart.objects.filter(product_id=product_id, u_id=user_id).first().delete()
#                 cart_items = Cart.objects.filter(u_id=user_id)
#                 serializer = CartSerializer(cart_items, many=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#
#             # Retrieve the cart item
#             cart_item = Cart.objects.get(product_id=product_id, u_id=user_id)
#
#             # Ensure quantity is greater than 1 before decrementing
#             if cart_item.quantity > 1:
#                 # Decrement quantity
#                 cart_item.quantity -= 1
#                 cart_item.save()
#
#                 # Update total price
#                 cart_item.price = cart_item.product_id.item_new_price * cart_item.quantity
#                 cart_item.save()
#
#                 cart_items = Cart.objects.filter(u_id=user_id)
#                 serializer = CartSerializer(cart_items, many=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 cart_item.delete()
#                 cart_items = Cart.objects.filter(u_id=user_id)
#                 serializer = CartSerializer(cart_items, many=True)
#                 return Response({"error": "Quantity cannot be less than 1." ,"status":0, "data": serializer.data}, status=status.HTTP_200_OK)
#         except Cart.DoesNotExist:
#             return Response({"error": "Cart item does not exist." ,"status":0}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#new
class DecreaseQuantityMain(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Retrieve product_id, user_id, and action from the request
            product_id = request.data.get('product_id')
            user_id = request.data.get('user_id')
            action = request.data.get('action')

            # Ensure user_id is provided
            # if not user_id:
            #     return Response({"error": "User ID parameter is required"}, status=400)

            # Check if user exists
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "User does not exist."}, status=404)

            # Check if wallet exists for the user

            if action == 'remove':
                # If action is 'remove', delete the cart item
                Cart.objects.filter(product_id=product_id, u_id=user_id).first().delete()


                # Get the updated list of cart items
                cart_items = Cart.objects.filter(u_id=user_id)
                serializer = CartSerializer(cart_items, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Retrieve the cart item
            cart_item = Cart.objects.get(product_id=product_id, u_id=user_id)
            try:
                wallet = Walet.objects.get(user_id=cart_item.u_id.id)
                wallet_value = wallet.wallet_value  # Get the wallet value before deleting

                # Delete the wallet
                wallet.delete()

                # Add wallet value back to CustomUser's walet
                # new
                # user.walet += wallet_value
                # user.save()
                pass

                # return Response({"success": "Wallet deleted successfully and amount added back to user's wallet."},
                #                 status=200)

            except Walet.DoesNotExist:
                pass
            # Ensure quantity is greater than 1 before decrementing
            if cart_item.quantity > 1:
                # Decrement quantity
                cart_item.quantity -= 1
                cart_item.save()

                # Update total price based on the new quantity
                cart_item.price = cart_item.product_id.item_new_price * cart_item.quantity
                cart_item.save()

                # Get the updated list of cart items
                cart_items = Cart.objects.filter(u_id=user_id)
                serializer = CartSerializer(cart_items, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # If quantity is 1 or less, delete the cart item
                cart_item.delete()

                # Get the updated list of cart items
                cart_items = Cart.objects.filter(u_id=user_id)
                serializer = CartSerializer(cart_items, many=True)
                return Response({
                    "error": "Quantity cannot be less than 1.",
                    "status": 0,
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"error": "Cart item does not exist.", "status": 0}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CartDetailsMainAPIView(APIView):
    permission_classes = []  # uncomment for no auth

    def get(self, request):
        try:
            print("✅ get_cart/main/ endpoint hit")
            user_id = request.query_params.get('user_id')
            product_id = request.query_params.get('product_id')

            if not user_id:
                return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            cart_items = Cart.objects.filter(u_id=user_id, product_id=product_id)

            serializer = CartGetSerializer(cart_items, many=True)

            if not serializer.data:
                return Response({"error": "No cart items found"}, status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data[0], status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UniqueProductCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')

            # Query the Cart table to get the count of unique products for the given user_id
            unique_product_count = Cart.objects.filter(u_id=user_id).values('product_id').distinct().count()
            return Response({'unique_product_count': unique_product_count}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'User does not have any products in the cart.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)