from django.db import models
from . models import NewCart,Product
from .serializers import CartSerializer, serializers
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.response import Response



class AddItemToCart(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        data = request.data
        
        try :
            product = Product.objects.get(id=data['product'])
        except Product.DoesNotExist:
            return Response({"message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)    
        
        try:
            cart_item = NewCart.objects.get(
                userId=user,
                product=product,
                                         
                                        )
        
            cart_item.quantity += data.get("quantity", 1)
            cart_item.save()
            return Response({"message": "Item updated successfully"}, status=status.HTTP_201_CREATED)
        
        except NewCart.DoesNotExist:
                NewCart.objects.create(
                    userId=user,
                    product=product,
                    quantity=data.get("quantity", 1)
                )
                return Response({"message": "Item add successfully"}, status=status.HTTP_201_CREATED)
                
class RemoveItemFromCart(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        user = request.user
        cart_id = request.query_params.get("id")
        
        if not cart_id:
            return Response({"message": "Cart id is required"}, status=status.HTTP_400_BAD_REQUEST)    
        
        cart_items = NewCart.objects.filter(userId=user)
        
        if not cart_items.filter(id=cart_id).exists():
            return Response({"message": "Cart item does not exist"}, status=status.HTTP_404_NOT_FOUND)
        cart_items.filter(id=cart_id).delete()
        return Response({"message": "Item removed successfully"}, status=status.HTTP_204_NO_CONTENT)

class CartCount(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        cart_count = NewCart.objects.filter(userId=user).count()
        return Response({"cart_count": cart_count}, status=status.HTTP_200_OK)
    
class UpdateCartItemQuantity(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch (self, request):
        item_id = request.query_params.get("id")
        count = request.query_params.get("count")
        cart_item = get_object_or_404(NewCart, id=item_id)
        cart_item.quantity = count
        cart_item.save()
        return Response({"message": "Item quantity updated successfully"}, status=status.HTTP_200_OK)
       

class GetUserCart(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer 
    
    def get(self, request):
        user = request.user
        cart_items = NewCart.objects.filter(userId=user).order_by('-createdAt')
        serializers = CartSerializer(cart_items, many=True)
        return Response(serializers.data)
        
        
        
                       