from rest_framework import serializers
from . import models
from core.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = models.NewCart
        exclude = ['userId','createdAt','updatedAt']
        