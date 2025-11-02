from django.urls import path
from . import views

app_name = 'theme'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('search-properties/', views.search_properties, name='search_properties'),
    # Project detail - redirect to Projects app
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('land/', views.land_page, name='land_page'),
    path('requirements/', views.requirements_page, name='requirements_page'),  # Changed from investment
    path('investment/', views.investment_page, name='investment_page'),  # New investment page
    # Interior page moved to interior app
    path('contact-us/', views.contact_us, name='contact_us'),

    # About Us page
    path('about-us/', views.about_us, name='about_us'),
    
    # Form submissions
    path('land-requirement/', views.land_requirement, name='land_requirement'),
    path('requirements-submission/', views.requirements_submission, name='requirements_submission'),  # Changed
    path('investment-requirement/', views.investment_requirement, name='investment_requirement'),
    
    # AJAX endpoints
    path('increment-views/<slug:slug>/', views.increment_project_views, name='increment_project_views'),
    path('ajax/project-types/', views.ajax_project_types, name='ajax_project_types'),

    # Legal pages
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    
    # PWA routes
    path('manifest.json', views.serve_manifest, name='manifest'),
    path('sw.js', views.serve_sw, name='service_worker'),
    path('offline/', views.offline_page, name='offline'),
]
