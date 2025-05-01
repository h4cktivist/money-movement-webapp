from django.urls import path

from . import views


urlpatterns = [
    path('', views.get_transactions, name='transaction_list'),
]
