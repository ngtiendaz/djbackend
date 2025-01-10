from rest_framework import serializers
from .import models


class WishListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source="product.title")
    price = serializers.ReadOnlyField(source="product.price")
    description = serializers.ReadOnlyField(source="product.description")
    is_featured = serializers.ReadOnlyField(source="product.is_featured")
    productType = serializers.ReadOnlyField(source="product.productType")
    rating = serializers.ReadOnlyField(source="product.rating")
    imageUrls = serializers.ReadOnlyField(source="product.imageUrls")
    createdAt = serializers.ReadOnlyField(source="product.createdAt")
    category = serializers.ReadOnlyField(source="product.category_id")
    brand = serializers.ReadOnlyField(source="product.brand_id")
    
    
    class Meta:
        model = models.NewWishlist
        fields = ['id',
                'title',
                'price',
                'description',
                'is_featured',
                'productType',
                'rating',
                'imageUrls',
                'createdAt',
                'category',
                'brand',
                ]