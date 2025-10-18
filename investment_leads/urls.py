from django.urls import path
from . import views

urlpatterns = [
    path('requirement/<int:requirement_id>/detail/', views.investment_requirement_detail_view, name='investment_requirement_detail'),
]
