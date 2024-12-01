from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from datetime import datetime
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm

#to list expenses
def expense_list(request):
    expenses = Expense.objects.all()

    current_month = datetime.now().month
    current_year = datetime.now().year

    total_expense = Expense.objects.filter(date__year=current_year, date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0

    category_expenses = (
        Expense.objects.filter(date__year=current_year, date__month=current_month)
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    categories = [item['category__name'] for item in category_expenses]
    totals = [float(item['total']) for item in category_expenses]

    return render(request, 'tracker/expense_list.html', {
        'expenses': expenses,
        'total_expense': total_expense,
        'categories': categories,
        'totals': totals,
    })


#to add  new expense
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

#to edit an existing expense
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/edit_expense.html', {'form': form})

#to delete an expense
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})
