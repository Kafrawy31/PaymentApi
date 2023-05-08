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



class Transaction(models.Model):
    transaction_id = models.UUIDField(default = uuid.uuid4, unique=True, editable = False, db_index=True)
    #merchant_id -- get from merchant
    date_created = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits = 9, decimal_places=2) #get from merchant
    user_transaction = models.ForeignKey(testUser, on_delete=models.CASCADE, blank = True, null = True)
    last_4_digits = models.CharField(max_length=4, null=True, blank=True)
    service = models.CharField(default = 'PayPal', editable=False, max_length=6)
    status = models.CharField(default = 'Outstanding', max_length=16)



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

class TestOrder(models.Model):
    itemId = models.IntegerField(primary_key=True,unique=True)
    itemName = models.CharField(max_length=30)
    itemCode = models.CharField(max_length=26)
    itemPrice = models.CharField(max_length=22)

