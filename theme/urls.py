from django.urls import path
from . import views

app_name = 'theme'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('search-properties/', views.search_properties, name='search_properties'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('land/', views.land_page, name='land_page'),
    path('investment/', views.investment_page, name='investment_page'),
    path('contact-us/', views.contact_us, name='contact_us'),
    
    # Form submissions
    path('land-requirement/', views.land_requirement, name='land_requirement'),
    path('investment-requirement/', views.investment_requirement, name='investment_requirement'),
    
    # AJAX endpoints
    path('increment-views/<int:project_id>/', views.increment_project_views, name='increment_project_views'),
    path('ajax/project-types/', views.ajax_project_types, name='ajax_project_types'),

    # Legal pages
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
