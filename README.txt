
To run locally
1.) Launch the command prompt
2.) git clone https://github.com/Kafrawy31/PaymentApi
3.) cd ./env
4.) cd./ scripts
5.) activate.ps1
6.) cd ..
7.) cd ..
8.) cd ./Payment
9.) python manage.py makemigrations Service
10.) python manage.py migrate
11.) python manage.py runserver

-----------------End-points-----------------
http://localhost:8000/PayApi/cards/ - shows all cards
http://localhost:8000/PayApi/newcard/ - create new card
http://localhost:8000/PayApi/newuser/ - create new user
http://localhost:8000/PayApi/usercards/userId/ - get all cards for a given user ID
http://localhost:8000/PayApi/usertransactions/userId/ - get all transactions for a given user ID
http://localhost:8000/PayApi/getuser/userID/ - get information for given user ID
http://localhost:8000/PayApi/newBA/ - billing address for pre-existing credit card
http://localhost:8000/PayApi/createTransaction/orderID/ - end-point for flight company to create transaction for given order
http://localhost:8000/PayApi/canceltransaction/transactionID - endpoint for refunding an existing transaction
http://localhost:8000/PayApi/createOrder/ - endpoint for flights to create order
http://localhost:8000/PayApi/main/ - launches command line interface and allows user to login, register cards and refund transactions

-----------------Suggested use Locally-----------------
1.) go to http://localhost:8000/PayApi/createOrder/ - and post the object below.
{
"itemName": "MIL FRA",
"price": 269.99,
"itemDescription": "27/05/2023 - MIL550" 
}
2.) The page will return the json object on the screen once posted, take the orderId and go to - http://localhost:8000/PayApi/createTransaction/orderID/ - with the orderID just returned{
    "user_id": 1,
    "order_id": THE ORDER ID JUST RETURNED
    "merchant_id": "1234",
    "delivery_email": "johndoe@example.com",
    "delivery_name": "John Doe",
    "transaction_amount": 99.99
}
3.) Once you post this request, the command line will prompt you to login and create a new card or use an existing one, user ID 1 - has one registered cards and many transactions, user ID 2 has no cards and no transactions
4.) Interact with the command-line as instructed, once you are done the command line will shut down


To run on pythonanywhere
1.) go to sc21ae.pythonanywhere.com
2.) There are extra steps to interact with the command-line prompt on python anywhere
3.) All the api endpoints on python anywhere are exactly the same as running locally, with the exception of changing http://localhost:8000/ to https://sc21ae.pythonanywhere.com/
4.) create an order using the same order json in previous section
5.) create a transaction using the same json in previous section

---------------Running Command-line interface PythonAnywhere ----------
1.) Launch a bash console
2.) workon myvirtualenv
3.) cd PaymentApi
4.) cd Payment
5.) python manage.py shell
6.) Then run these commands in the shell
7.) import requests
8.) from django.test import RequestFactory
9.) from Service.views import main
10.) request = RequestFactory().get('/')
11.) response = main(request)
12.) interact with the command-line as instructed, once you are done the command-line will shut down

superuser credentials:
username: ammar
password: alaska123

PythonAnywhere domain:
sc21ae.pythonanywhere.com