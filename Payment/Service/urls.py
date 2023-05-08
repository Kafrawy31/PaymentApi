from django.urls import path
from . import views

urlpatterns = [
    path('cards/', views.cardView),
    path('main', views.main),
    path('newcard/', views.newCardView),
    path('newuser/', views.newUserView),
    path('usercards/<str:pk>/', views.userCardsView),
    path('usertransactions/<str:pk>/', views.userTransactions),
    path('getuser/<str:pk>/', views.getUserView),
    path('newBA/', views.newBillingAddress),
    path('newtransaction/',views.newTransactionView),
    path('canceltransaction/<str:pk>/',views.CancelTransaction),
]