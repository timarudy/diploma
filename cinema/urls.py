from django.urls.conf import path
from .views import *


urlpatterns = [
    path('homepage/', SessionListView.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('homepage/add-cinema/', CinemaAppend.as_view(), name='cinema_append'),
    path('homepage/add-session/', SessionAppend.as_view(), name='session_append'),
    path('homepage/ticket-purchase/<int:pk>/', TicketBuy.as_view(), name='purchase')
]