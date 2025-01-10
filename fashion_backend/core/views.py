from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers
from django.db.models import Count
import random
from rest_framework.permissions import IsAdminUser

# Create your views here.

class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = models.Product.objects.all()
        queryset = queryset.annotate(random_order=Count("id"))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]
    
class DeleteProduct(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request):
        try:
            pk = request.query_params.get("id")
            product = models.Product.objects.get(id=pk)
            product.delete()
            return Response({"message":"Product deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except models.Product.DoesNotExist:
            return Response({"message":"Product not found"},status=status.HTTP_404_NOT_FOUND)

class UpdateProduct(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request):
        try:
            pk = request.query_params.get("id")
            product = models.Product.objects.get(id=pk)

            # Lấy dữ liệu từ request để cập nhật sản phẩm
            data = request.data
            product.title = data.get("title", product.title)
            product.price = data.get("price", product.price)
            product.description = data.get("description", product.description)
            product.save()

            return Response(
                {"message": "Product updated successfully", "product": {
                    "id": product.id,
                    "title": product.title,
                    "price": product.price,
                    "description": product.description,
                }},
                status=status.HTTP_200_OK
            )
        except models.Product.DoesNotExist:
            return Response(
                {"message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
class ProductDetail(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        pk = request.query_params.get("id")
        product = models.Product.objects.get(id=pk)
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data)
    
class CreateProduct(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        data = request.data
        serializer = serializers.ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        return Response(  {"message": " Product creation failed"}, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class HomeCategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    def get_queryset(self):
        queryset = models.Category.objects.all()

        queryset = queryset.annotate(random_order=Count("id"))

        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:5]
    

class BrandList(generics.ListAPIView):
    serializer_class = serializers.BrandSerializer
    queryset = models.Brand.objects.all()

class PopularProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    def get_queryset(self):
        queryset = models.Product.objects.filter(ratings__gte=4.0, ratings__lte=5.0)
        queryset = queryset.annotate(random_order=Count("id"))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]
    
class ProductListByProductType(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    def get(self,request):
        query = request.query_params.get("productType",None)
        if query:
            queryset = models.Product.objects.filter(productType=query)
            # queryset = queryset.annotate(random_order=Count("id"))
            products_list = list(queryset)
            # random.shuffle(queryset)
            Linited_products = products_list[:20]
            serializer=serializers.ProductSerializer(Linited_products,many=True)
            
            return Response(serializer.data)
        else:
            return Response({"message":"No query provided"},status=status.HTTP_400_BAD_REQUEST)
    
class SimilarProducts(APIView):
    def get(self, request):
        query = request.query_params.get("category",None)

        if query:
            products = models.Product.objects.filter(category= query)

            product_List = list(products)
            random.shuffle(product_List)
            linited_products = product_List[:6]
            serializer=serializers.ProductSerializer(linited_products,many=True)
            
            return Response(serializer.data)
        else:
            return Response({"message":"No query provided"},status=status.HTTP_400_BAD_REQUEST)

class SearchProductByTitle(APIView):
    def get(self, request):
        query = request.query_params.get("q",None)

        if query:
            products = models.Product.objects.filter(title__icontains=query)

            serializer = serializers.ProductSerializer(products,many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"No query provided"},status=status.HTTP_400_BAD_REQUEST)

class FilterProductByCategory(APIView):
    def get(self, request):
        query = request.query_params.get("category",None)

        if query:
            products = models.Product.objects.filter(category_id=query)
            serializer = serializers.ProductSerializer(products,many=True)
            return Response(serializer.data)
        else:   
            return Response({"message":"No query provided"},status=status.HTTP_400_BAD_REQUEST)

