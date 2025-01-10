from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Product

class NewCart(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # productType = models.CharField(max_length=255,default="Văn phòng")
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return "{}/{}".format(self.userId.username, self.product.title)
