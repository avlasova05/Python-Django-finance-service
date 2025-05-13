from django.db import migrations


def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('main', 'Category')

    # Общие категории расходов
    common_expense_categories = [
        'Еда', 'Транспорт', 'Жилье', 'Развлечения', 'Одежда'
    ]

    # Общие категории доходов
    common_income_categories = [
        'Зарплата', 'Фриланс', 'Инвестиции', 'Подарки'
    ]

    for name in common_expense_categories:
        Category.objects.get_or_create(
            name=name,
            category_type='expense',
            user=None
        )

    for name in common_income_categories:
        Category.objects.get_or_create(
            name=name,
            category_type='income',
            user=None
        )


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),  # Зависит от вашей первой миграции
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]