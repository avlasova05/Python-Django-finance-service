from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Expense, Income, Category, SavingsGoal
import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO
from datetime import datetime
from collections import defaultdict
from .forms import ExpenseForm, IncomeForm, SavingsGoalForm, AddToSavingsForm
from django.contrib import messages
import matplotlib
matplotlib.use('Agg')  #  бэкенд, не требующий GUI
import matplotlib.pyplot as plt



def index(request):
    return render(request, 'main/index.html')
def news_home(request):
    return render(request, 'news/features.html' )

def about(request):
    return render(request, 'main/about.html')


@login_required
def personal_finance_view(request):  # Переимен функцию
    # Генерация круговой диаграммы расходов
    expenses = Expense.objects.filter(user=request.user)
    expense_data = defaultdict(float)
    for expense in expenses:
        expense_data[expense.category.name] += float(expense.amount)

    plt.figure(figsize=(6, 6))
    plt.pie(expense_data.values(), labels=expense_data.keys(), autopct='%1.1f%%')
    plt.title('Распределение расходов')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    pie_chart = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Подготовка данных для месячного графика
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    income_data = [0] * 12
    expense_data = [0] * 12

    current_year = datetime.now().year
    incomes = Income.objects.filter(user=request.user, date__year=current_year)
    expenses = Expense.objects.filter(user=request.user, date__year=current_year)

    for income in incomes:
        month = income.date.month - 1
        income_data[month] += float(income.amount)

    for expense in expenses:
        month = expense.date.month - 1
        expense_data[month] += float(expense.amount)

    months_data = {
        'labels': months,
        'income': income_data,
        'expenses': expense_data
    }

    #  расчет общей статистики
    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.amount for expense in expenses)
    balance = total_income - total_expenses

    current_month = datetime.now().date().replace(day=1)
    savings_goal = SavingsGoal.objects.filter(user=request.user, month=current_month).first()

    # Инициализация форм
    goal_form = SavingsGoalForm(initial={'month': current_month})
    add_form = AddToSavingsForm()

    if request.method == 'POST':
        if 'set_goal' in request.POST:
            goal_form = SavingsGoalForm(request.POST)
            print("\n=== DEBUG SAVINGS GOAL FORM ===")
            print("Form data:", request.POST)
            print("Form is valid:", goal_form.is_valid())
            if not goal_form.is_valid():
                print("Form errors:", goal_form.errors)
            print("=======================\n")
            if goal_form.is_valid():
                try:
                    goal = goal_form.save(commit=False)
                    goal.user = request.user
                    goal.month = goal.month.replace(day=1)
                    goal.save()
                    messages.success(request, 'Цель успешно установлена!')
                    return redirect('personal_finance')
                except Exception as e:
                    messages.error(request, f'Ошибка при сохранении цели: {str(e)}')
        elif 'add_to_savings' in request.POST:
            add_form = AddToSavingsForm(request.POST)
            if add_form.is_valid():
                if savings_goal:
                    amount = add_form.cleaned_data['amount']
                    savings_goal.current_amount += amount
                    savings_goal.save()
                    messages.success(request, f'Успешно добавлено {amount} руб. к накоплениям!')
                else:
                    messages.error(request, 'У вас нет активной цели накоплений!')
                return redirect('personal_finance')

    return render(request, 'main/personal_finance.html', {
        'pie_chart': pie_chart,
        'months_data': months_data,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'current_year': current_year,
        'user': request.user,
        'savings_goal': savings_goal,
        'goal_form': goal_form,
        'add_form': add_form,
    })


@login_required
def edit_savings_goal(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, user=request.user)

    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Цель успешно обновлена!')
            return redirect('personal_finance')
    else:
        form = SavingsGoalForm(instance=goal)

    return render(request, 'main/edit_savings_goal.html', {
        'form': form,
        'goal': goal,
    })


@login_required
def delete_savings_goal(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Цель успешно удалена!')
    return redirect('personal_finance')
@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(data=request.POST, user=request.user)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Доход успешно добавлен!')
            return redirect('personal_finance')
    else:
        form = IncomeForm(user=request.user)

    return render(request, 'main/add_transaction.html', {
        'form': form,
        'title': 'Добавление дохода'

    })


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)  # Правильный способ
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Расход успешно добавлен!')
            return redirect('personal_finance')
    else:
        form = ExpenseForm(user=request.user)

    return render(request, 'main/add_transaction.html', {
        'form': form,
        'title': 'Добавление расхода'
    })
def financial_tips(request):
    tips = [
        {"title": "Бюджетирование", "content": "Ведите учет доходов и расходов, планируйте бюджет на месяц."},
        {"title": "Накопления", "content": "Откладывайте минимум 10-20% от каждого дохода."},
        {"title": "Инвестиции", "content": "Диверсифицируйте вложения, не храните все деньги в одном месте."},
        {"title": "Кредиты", "content": "Берите кредиты только на действительно важные цели и только если уверены в платежеспособности."},
        {"title": "Финансовая подушка", "content": "Создайте резервный фонд на 3-6 месяцев жизни."},
    ]
    return render(request, 'main/financial_tips.html', {'tips': tips})


