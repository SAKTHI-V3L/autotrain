# timeseries/urls.py
from django.urls import path
from . import views

app_name = 'timeseries'  # This defines the namespace

urlpatterns = [
    path('upload_dataset/', views.upload_dataset, name='upload_dataset'),
    path('train_model/', views.train_model, name='train_model'),
    path('model_result/', views.model_result, name='model_result')
]
