from rest_framework import serializers
from . import models

class NoficationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nofication
        fields = "__all__"
        
            