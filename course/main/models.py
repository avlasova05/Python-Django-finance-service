from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    CATEGORY_TYPE = (
        ('income', 'Доход'),
        ('expense', 'Расход'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=7, choices=CATEGORY_TYPE)

    def __str__(self):
        return f"{self.get_category_type_display()}: {self.name}"


class Expense(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # Разрешить NULL в базе данных
        blank=True  # Разрешить пустое значение в формах
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 limit_choices_to={'category_type': 'expense'})
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.date})"


class Income(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 limit_choices_to={'category_type': 'income'})
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.date})"


class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Накопления")
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month = models.DateField()  # Будем хранить первый день месяца
    created_at = models.DateTimeField(auto_now_add=True)

    def remaining_amount(self):
        return self.target_amount - self.current_amount

    def progress_percentage(self):
        return (self.current_amount / self.target_amount) * 100 if self.target_amount > 0 else 0

    def __str__(self):
        return f"{self.name} ({self.month.strftime('%B %Y')}) - {self.current_amount}/{self.target_amount}"