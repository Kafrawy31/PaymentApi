from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"
        
class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = "__all__"


class testUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = testUser
        fields = "__all__"
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"