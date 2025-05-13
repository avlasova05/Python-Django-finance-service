from .models import Funcs
from django.forms import ModelForm, TextInput, DateInput, Textarea, CheckboxInput
from .models import Features
class FuncsForm(ModelForm):
    class Meta:
        model = Funcs
        fields =['last_name', 'first_name',  'date', 'status']

        class FuncsForm(ModelForm):
            class Meta:
                model = Funcs
                fields = ['last_name',  'first_name', 'date', 'status']

                widgets = {
                    "last_name": TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Фамилия'
                    }),

                    "first_name": TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Имя'
                    }),
                    "date": DateInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Дата регистрации'
                    }),
                    "status": Textarea(attrs={
                        'class': 'form-control',
                        'placeholder': 'Статус пользователя'

                    })
                }

class FeaturesForm(ModelForm):
        class Meta:
            model = Features
            fields = ['name', 'description', 'is_active']

            widgets = {
                "name": TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
                "description": TextInput(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
                "is_active": CheckboxInput(attrs={'class': 'form-check-input'})
            }