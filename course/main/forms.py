from django import forms
from django.db import models
from django.db.models import Q
from .models import Expense, Income, Category, SavingsGoal
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'style': 'color: #000000;'}),
        label=mark_safe('<span style="color: white;">Дата</span>'),
    )

    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']
        labels = {
            'amount': mark_safe('<span style="color: white;">Сумма</span>'),
            'category': mark_safe('<span style="color: white;">Категория</span>'),
            'description': mark_safe('<span style="color: white;">Описание</span>'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  #  user из kwargs
        super().__init__(*args, **kwargs)  # Передаем оставшиеся аргументы


        for field_name, field in self.fields.items():
            if field_name != 'date':  # Дата уже настроена
                field.widget.attrs.update({'style': 'color: #000000;'})

        # категории по пользователю
        if user:
            self.fields['category'].queryset = Category.objects.filter(
                Q(category_type='expense') & (Q(user=user) | Q(user=None))
            )
        else:
            self.fields['category'].queryset = Category.objects.filter(
                category_type='expense',
                user=None
            )


class IncomeForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'style': 'color: #000000;'}),
        label=mark_safe('<span style="color: white;">Дата</span>'),
    )

    class Meta:
        model = Income
        fields = ['amount', 'category', 'description', 'date']
        labels = {
            'amount': mark_safe('<span style="color: white;">Сумма</span>'),
            'category': mark_safe('<span style="color: white;">Категория</span>'),
            'description': mark_safe('<span style="color: white;">Описание</span>'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            if field_name != 'date':
                field.widget.attrs.update({'style': 'color: #000000;'})


        if user:
            self.fields['category'].queryset = Category.objects.filter(
                Q(category_type='income') & (Q(user=user) | Q(user=None))
            )
        else:
            self.fields['category'].queryset = Category.objects.filter(
                category_type='income',
                user=None
            )

class SavingsGoalForm(forms.ModelForm):
    month = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month'}),
        help_text="Выберите месяц и год"
    )

    class Meta:
        model = SavingsGoal
        fields = ['name', 'target_amount', 'month']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название цели'}),
            'target_amount': forms.NumberInput(attrs={'placeholder': 'Целевая сумма'}),
        }

class AddToSavingsForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Сумма для добавления'
            }
        )
    )