from rest_framework import serializers, generics, permissions, status
from quotes.models import *
from rest_framework.serializers import ModelSerializer


from rest_framework import serializers
from django.contrib.auth import authenticate

    
class DeliverySerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'  