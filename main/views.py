from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Transaction, TransactionType, Category, Subcategory, Status
from .forms import TransactionForm


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


def get_categories(request):
    transaction_type_id = request.GET.get('transaction_type_id')
    selected = request.GET.get('selected')

    categories = Category.objects.filter(transaction_type_id=transaction_type_id)

    context = {
        'categories': categories,
        'selected': selected,
    }
    return render(request, 'includes/_category_options.html', context)


def get_subcategories(request):
    category_id = request.GET.get('category_id')
    selected = request.GET.get('selected')

    subcategories = Subcategory.objects.filter(category_id=category_id)

    context = {
        'subcategories': subcategories,
        'selected': selected,
    }
    return render(request, 'includes/_subcategory_options.html', context)


def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            messages.success(request, 'Операция успешно создана!')
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    context = {
        'form': form
    }
    return render(request, 'transaction_form.html', context)


def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Операция успешно обновлена!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)

    context = {
        'form': form,
        'transaction': transaction,
    }
    return render(request, 'transaction_form.html', context)


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Операция успешно удалена!')
        return redirect('transaction_list')

    context = {
        'transaction': transaction,
    }
    return render(request, 'transaction_confirm_delete.html', context)
