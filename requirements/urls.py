from django.urls import path
from . import views

app_name = 'requirements'

urlpatterns = [
    path('submit/', views.requirement_submission, name='requirement_submission'),
]
