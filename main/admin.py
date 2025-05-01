from django.contrib import admin

from .models import Status, Category, Subcategory, TransactionType, Transaction


admin.site.register(Status)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(TransactionType)
admin.site.register(Transaction)
