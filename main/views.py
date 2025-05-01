from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Transaction, TransactionType, Category, Subcategory, Status


def get_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    transaction_type_id = request.GET.get('transaction_type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    if status_id:
        transactions = transactions.filter(status_id=status_id)
    if transaction_type_id:
        transactions = transactions.filter(transaction_type_id=transaction_type_id)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if subcategory_id:
        transactions = transactions.filter(subcategory_id=subcategory_id)

    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'transactions': page_obj,
        'statuses': Status.objects.all(),
        'transaction_types': TransactionType.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }

    return render(request, 'transaction_list.html', context)
