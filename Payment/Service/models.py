from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
import uuid
from django.core.validators import RegexValidator
from datetime import datetime
#get user from database


class testUser(models.Model):
    userId = models.BigAutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=16)
    def __str__(self):
        return self.username
    
    

class Card(models.Model):
    card_number_format_validator = RegexValidator(
        regex=r'^\d{4}\-\d{4}\-\d{4}\-\d{4}$',
        message='Card number must be in the format "xxxx-xxxx-xxxx-xxxx" where x is a number'
    )
    
    cvv_number_format_validator = RegexValidator(
        regex=r'^\d{3,4}$',
        message='CVV number must be either 3 or 4 digits.'
    )
    
    expiry_date_format_validator = RegexValidator(
        regex=r'^\d{2}/\d{4}$',
        message='Expiry date must be in the format "MM/YYYY".'
    )
    #add card ID
    card_number = models.CharField(max_length=19, 
                                   null=False, blank = False, 
                                   primary_key=True, unique=True, 
                                   validators=[card_number_format_validator],)
    cvv = models.CharField(validators=[MinLengthValidator(3), cvv_number_format_validator], max_length=4, null=False, blank=False)
    expiry_date = models.CharField(null=False, blank = False, max_length=16)
    name_on_card = models.CharField(max_length=26)
    user_card = models.ForeignKey(testUser, on_delete=models.CASCADE, blank=True,null=True)
    last_4_digits = models.CharField(max_length=4, null=True, blank=True, editable=False)
    
    
    def save(self, *args, **kwargs):
        if not self.last_4_digits:  
            self.last_4_digits = self.card_number[-4:]
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name_on_card







class BillingAddress(models.Model):
    card = models.OneToOneField(
        Card,
        on_delete=models.CASCADE,
        primary_key=True)
    full_name = models.CharField(max_length=36, null=False, blank=False)
    address_1 = models.CharField(max_length=50, null= False, blank=False)
    address_2 = models.CharField(max_length=50, blank= True)
    city = models.CharField(max_length=20, null = False , blank=False)
    postcode = models.CharField(max_length=10, null=False, blank= False)
    region = models.CharField(max_length=26, null=False, blank= False)
    country = models.CharField(max_length=40, null=False, blank= False)
    

## Order class, get from merchant database

class Order(models.Model):
    orderId = models.BigAutoField(primary_key=True,unique=True)
    itemName = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    itemDetails = models.CharField(max_length=50)
    
class Transaction(models.Model):
    transaction_id = models.UUIDField(default = uuid.uuid4, unique=True, editable = False, db_index=True)
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    user_id = models.ForeignKey(testUser, on_delete=models.CASCADE, blank = True, null = True)
    merchant_id = models.CharField(max_length=50, null=True, blank =True)
    delivery_email = models.EmailField(max_length=30, null=True, blank=True)
    delivery_name = models.CharField(max_length=30, blank= True, null=True)
    transaction_amount = models.DecimalField(max_digits = 9, decimal_places=2) 
    service = models.CharField(default = 'PayPal', editable=False, max_length=6)
    status = models.CharField(default = 'Outstanding', max_length=16)
    date_created = models.DateTimeField(auto_now_add=True)
    
    @property
    def transaction_amount(self):
        return self.order_id.price
    



