from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import *
from .Serializers import *
import re
from django.http import HttpResponse, HttpResponseNotFound
import requests
import json
from rest_framework import status
from rest_framework.exceptions import NotFound
# Create your views here.

def get_user_cards(pk):
    user_cards = Card.objects.filter(user_card=pk)
    return user_cards

def get_current_order(pk):
    curr_order = TestOrder(itemId = pk)
    return curr_order

def main(request,orderurl,ordernum):

    response = requests.get(f"http://localhost:8000/{orderurl}/{ordernum}")
    order = response.json()
    price = order['itemPrice']
    print("You are paying for this item")
    print("ITEM ID:" , order['itemId'])
    print("ITEM PRICE:" , order['itemPrice'])
    

    user = False
    while user == False:
        curr = input("please enter your userID \n")
        response = requests.get(f"http://localhost:8000/PayApi/getuser/{curr}/")
        if response.status_code == 200:
            print("User Found")
            card_list = response.json()
            user = True
        else:
            print("User not found\n")
            new_user_choice = input('Would you like to create a new user? (y/n): ')
            if new_user_choice == 'y':
                username = input('Please enter your username: ')
                new_user = {
                    'username': username,
                }
                response = requests.post("http://localhost:8000/PayApi/newuser/", data=new_user)
            else:
                print("\n")
                
                
            
            
    response = requests.get(f"http://localhost:8000/PayApi/usercards/{curr}/")
    card_list = response.json()
    count = 1

    
    paid = False
    while paid == False:
        choice = input("would you like to use a registered card, (y/n)? If there are no registered cards you will be prompted to create a new one:  ")
        if choice == "n" or len(card_list) == 0:
            print("enter the details of the new card")
            card_pattern = "(\d\d\d\d)-(\d\d\d\d)-(\d\d\d\d)-(\d\d\d\d)"
            card_number_input = input('Enter card number (format "xxxx-xxxx-xxxx-xxxx"): ')
            while True:
                if not (re.search(card_pattern, card_number_input)):
                    print('The number you entered is not a valid card number, please enter the number in this format "xxxx-xxxx-xxxx-xxxx" \n')
                    card_number_input = input('Enter card number (format "xxxx-xxxx-xxxx-xxxx"): ')
                else:
                    print('\n')
                    break

            cvv_pattern = r'^\d{3,4}$'  
            cvv_input = input('Enter CVV number (3 or 4 digits): ')
            while True:
                if not (re.search(cvv_pattern, cvv_input)):
                    print("The CVV you entered is not a valid CVV number, please enter a 3 or 4 digit number \n")
                    cvv_input = input('Enter CVV number (3 or 4 digits): ')
                else:
                    print('\n')
                    break
                    

            expiry_date_pattern = r'^\d{2}/\d{4}$'
            while True:
                expiry_date_input = input('Enter expiry date (format "MM/YYYY"): ')
                if not (re.search(expiry_date_pattern, expiry_date_input)):
                    print('The expiry date you entered is not a valid expiry date, please enter the date in this format (MM/YYYY): \n')
                else:
                    try:
                        expiry_date_input = datetime.strptime(expiry_date_input, '%m/%Y').date()
                        break  # Exit the loop if input is valid
                    except ValueError:
                        print('Invalid date format. Please enter date in format MM/YYYY. \n')
                

            
            name_pattern = r'^\w+\s\w+$'
            while True:
                name_on_card_input = input('Enter name on card: ')
                if not(re.search(name_pattern,name_on_card_input)):
                    print("please enter the name in this format: Firstname Lastname")
                else:
                    card_number_temp = card_number_input
                    break

            print("-------------------- BILLING ADDRESS DETAILS --------------------")
            while True:
                billing_name = input('Please enter your name: ')
                if not(re.search(name_pattern,billing_name)):
                    print("please enter the name in this format: Firstname Lastname")
                else:
                    break
                
            while True:
                address_1_input = input('Please enter first address: ')
                if address_1_input == "":
                    print("This field is required\n")
                else:
                    break
                
            address_2_input = input('Please enter second address line, you can leave this empty: ')

            while True:
                city_input = input('Please enter city: ')
                if city_input == "":
                    print("This field is required \n")
                else:
                    break

            post_code_pattern = r'^[a-zA-Z0-9]{3,5}\s[a-zA-Z0-9]{1,4}$'
            while True:
                post_code_input = input('Please enter post code: ')
                if not(re.search(post_code_pattern, post_code_input)):
                    print("Please enter a valid post code:")
                else:
                    break

            while True:
                region_input = input('Please enter region: ')
                if region_input == "":
                    print("This field is required \n")
                else:
                    break
                
            while True:
                country_input = input('Please enter country: ')
                if country_input == "":
                    print("This field is required \n")
                else:
                    break

            new_card = {
                'card_number' : card_number_input,
                'cvv':cvv_input,
                'user_card' : curr,
                'expiry_date':expiry_date_input,
                'name_on_card' :name_on_card_input
            }
            response = requests.post('http://localhost:8000/PayApi/newcard/',data=new_card)
            
            new_billing_address = {
                'card' : card_number_temp,
                'full_name' : billing_name,
                'address_1' : address_1_input,
                'address_2' : address_2_input,
                'city' : city_input,
                'postcode' : post_code_input,
                'region' : region_input,
                'country' : country_input
            }
            response = requests.post('http://localhost:8000/PayApi/newBA/',data=new_billing_address)            

            new_transaction = {
                'card' : card_number_temp,
                'amount_paid' : 200,
                'user_transaction' : curr,
                'last_4_digits' : card_number_temp[-4:],
                'status' : 'Paid',
            }
            response = requests.post('http://localhost:8000/PayApi/newtransaction/',data=new_transaction)
            paid = True
        
        ## to cancel, send patch to update status to cancelled, 
        ## get current user, get their balance, send money back to user.
          

                
            
        else:
            print("which card would you like to pay with \n")
                
            for i in card_list: 
                print(count, "Card ending with **",i.get('last_4_digits'))
                count+=1
            card_choice = int(input("enter the card you want to pay with 1\n"))
            card = card_list[card_choice-1]
            
            new_transaction = {
                'card' : card['card_number'],
                'amount_paid' : 200,
                'user_transaction' : curr,
                'last_4_digits' : card['last_4_digits'],
                'status' : 'Paid',
            }
            response = requests.post('http://localhost:8000/PayApi/newtransaction/',data=new_transaction)
            paid = True

    cancel = True
    while cancel == True:
        cancel_transaction_choice = input("Would you like to refund/cancel any transaction made on your account (y/n)?")
        if cancel_transaction_choice == 'y':
            response = requests.get(f"http://localhost:8000/PayApi/usertransactions/{curr}/")
            transaction_list = response.json()
            transaction_count = 1
            for i in transaction_list:
                print(transaction_count, "Transaction: ",i.get('transaction_id'), "Amount: ",i.get('amount_paid'), "Status: ", i.get('status'))
                transaction_count += 1
            transaction_choice = int(input("Which transaction do you wish to refund? "))
            transaction = transaction_list[transaction_choice - 1]
            
            transaction_cancel = {
                "status" : "Cancelled",
            }
            
            response = requests.patch(f"http://localhost:8000/PayApi/canceltransaction/{transaction['transaction_id']}/", data=transaction_cancel)
        else:
            return HttpResponse("Thank you for using this payment system")
    
        
   


@api_view(["GET"])
def cardView(request):
    cards = Card.objects.all()
    serializer = CardSerializer(cards, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def newCardView(request):
    serializer = CardSerializer(data=request.data)  
    if serializer.is_valid(): 
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def newUserView(request):
    serializer = testUserSerializer(data=request.data)  
    if serializer.is_valid(): 
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def newBillingAddress(request):
    serializer = BillingAddressSerializer(data=request.data)  
    if serializer.is_valid(): 
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['POST'])
def newTransactionView(request):
    serializer = TransactionSerializer(data=request.data)  
    if serializer.is_valid(): 
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def transactionView(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer
    return Response(serializer.data)

@api_view(['GET'])
def userCardsView(request,pk):
    uCards = Card.objects.filter(user_card=pk)
    serializer = CardSerializer(uCards, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def userTransactions(request,pk):
    uTransactions = Transaction.objects.filter(user_transaction=pk)
    serializer = TransactionSerializer(uTransactions, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def chosenCard(request,pk):
    cCard = Card.objects.get(card_number = pk)
    serializer = CardSerializer(cCard, many = False)
    return Response(serializer.data)


@api_view(['GET'])
def getUserView(request, pk):
    try:
        tUser = testUser.objects.get(userId=pk)
    except testUser.DoesNotExist:
        return HttpResponseNotFound("User with ID {} does not exist".format(pk))
    
    serializer = testUserSerializer(tUser, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteCard(request,pk):
    card = Card.objects.get(card_number = pk)
    card.delete()
    return Response('ITEM DELETED SUCCESFULLY')

@api_view(['PATCH'])
def CancelTransaction(request,pk):
    transaction = Transaction.objects.get(transaction_id=pk)
    serializer = TransactionSerializer(instance = transaction, data=request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
