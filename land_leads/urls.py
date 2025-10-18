from django.urls import path
from . import views

urlpatterns = [
    path('requirement/<int:requirement_id>/detail/', views.land_requirement_detail_view, name='land_requirement_detail'),
]
