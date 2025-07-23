from django.urls import path, include 
from . import views
 

urlpatterns = [ 
    path('', views.index, name='index'),
    path('project/<int:project_id>/detail/', views.project_detail_view, name='project_detail'),
    # PDF download route removed
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('ajax/get-project-types/', views.get_project_types, name='get_project_types'),
] 
