from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_home, name='news_home'),
    path('news/create/', views.create, name='create'),
    path('news/features/', views.features_list, name='features_list'),
    path('news/features/create/', views.create_feature, name='create_feature'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.home_view, name='home')
]