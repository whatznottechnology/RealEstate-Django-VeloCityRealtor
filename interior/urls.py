from django.urls import path
from . import views

app_name = 'interior'

urlpatterns = [
    path('', views.interior_page, name='interior_page'),
    path('submit-inquiry/', views.submit_inquiry_ajax, name='submit_inquiry_ajax'),
]
