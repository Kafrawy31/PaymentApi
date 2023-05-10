from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('cards/', views.cardView),
    path('main', views.main),
    path('newcard/', views.newCardView),
    path('newuser/', views.newUserView),
    path('usercards/<str:pk>/', views.userCardsView),
    path('usertransactions/<str:pk>/', views.userTransactions),
    path('getuser/<str:pk>/', views.getUserView),
    path('newBA/', views.newBillingAddress),
    path('createTransaction/<str:order_id>', newTransaction.as_view()),
    path('canceltransaction/<str:pk>/',views.CancelTransaction),
    path('createOrder/',views.createOrderView),
]