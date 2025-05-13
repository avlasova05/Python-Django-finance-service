from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import personal_finance_view, add_income, add_expense, financial_tips


urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('personal-finance/', personal_finance_view, name='personal_finance'),
    path('add_income/', add_income, name='add_income'),
    path('add_expense/', add_expense, name='add_expense'),
    path('financial_tips/', financial_tips, name='financial_tips'),
    path('savings-goal/edit/<int:goal_id>/', views.edit_savings_goal, name='edit_savings_goal'),
    path('savings-goal/delete/<int:goal_id>/', views.delete_savings_goal, name='delete_savings_goal'),
]