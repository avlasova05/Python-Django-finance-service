from django.db import models


class Funcs(models.Model):
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    date = models.DateField(verbose_name='Дата')
    status = models.CharField(max_length=100,verbose_name='Статус')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Features(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название функции')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return self.name