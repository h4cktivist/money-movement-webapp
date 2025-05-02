from django.urls import path

from . import views


urlpatterns = [
    path('', views.get_transactions, name='transaction_list'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('<int:pk>/edit/', views.transaction_update, name='transaction_update'),
    path('<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),

    path('references/', views.reference_management, name='reference_management'),
    path('references/delete/<str:model_name>/<int:pk>/', views.delete_reference_item, name='delete_reference_item'),
    path('references/edit/<str:model_name>/<int:pk>/', views.edit_reference_item, name='edit_reference_item'),

    path('get-categories/', views.get_categories, name='get_categories'),
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
]
