from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Transaction, TransactionType, Category, Subcategory, Status
from .forms import TransactionForm, TransactionTypeForm, CategoryForm, SubcategoryForm, StatusForm


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


def reference_management(request):
    if request.method == 'POST':
        status_form = StatusForm(request.POST, prefix='status')
        type_form = TransactionTypeForm(request.POST, prefix='type')
        category_form = CategoryForm(request.POST, prefix='category')
        subcategory_form = SubcategoryForm(request.POST, prefix='subcategory')

        if status_form.is_valid() and 'status_submit' in request.POST:
            status_form.save()
            messages.success(request, 'Статус успешно добавлен!')
            return redirect('reference_management')

        if type_form.is_valid() and 'type_submit' in request.POST:
            type_form.save()
            messages.success(request, 'Тип операции успешно добавлен!')
            return redirect('reference_management')

        if category_form.is_valid() and 'category_submit' in request.POST:
            category_form.save()
            messages.success(request, 'Категория успешно добавлена!')
            return redirect('reference_management')

        if subcategory_form.is_valid() and 'subcategory_submit' in request.POST:
            subcategory_form.save()
            messages.success(request, 'Подкатегория успешно добавлена!')
            return redirect('reference_management')
    else:
        status_form = StatusForm(prefix='status')
        type_form = TransactionTypeForm(prefix='type')
        category_form = CategoryForm(prefix='category')
        subcategory_form = SubcategoryForm(prefix='subcategory')

    context = {
        'statuses': Status.objects.all(),
        'types': TransactionType.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'status_form': status_form,
        'type_form': type_form,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
    }

    return render(request, 'reference_management.html', context)


def edit_reference_item(request, model_name, pk):
    models_map = {
        'status': (Status, StatusForm),
        'type': (TransactionType, TransactionTypeForm),
        'category': (Category, CategoryForm),
        'subcategory': (Subcategory, SubcategoryForm),
    }

    if model_name not in models_map:
        messages.error(request, 'Неверный тип справочника')
        return redirect('reference_management')

    model, form_class = models_map[model_name]
    item = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        form = form_class(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены успешно!')
            return redirect('reference_management')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = form_class(instance=item)

    context = {
        'form': form,
        'model_name': model_name,
        'item': item
    }
    return render(request, 'reference_item_edit.html', context)


def delete_reference_item(request, model_name, pk):
    models_map = {
        'status': Status,
        'type': TransactionType,
        'category': Category,
        'subcategory': Subcategory,
    }

    model = models_map.get(model_name)
    if not model:
        messages.error(request, 'Неверный тип справочника')
        return redirect('reference_management')

    item = get_object_or_404(model, pk=pk)
    item.delete()
    messages.success(request, 'Элемент справочника успешно удален!')

    return redirect('reference_management')
