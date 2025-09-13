def terms_and_conditions(request):
    return render(request, 'pages/terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')

def interior_page(request):
    """Interior services page view"""
    return render(request, 'pages/interior.html')

def about_us(request):
    # Get active developers for the developers section
    active_developers = Developer.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'active_developers': active_developers,
    }
    
    return render(request, 'pages/about_us.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from Projects.models import Project, Category, ProjectType, City, Amenity
from land_leads.models import LandRequirement
from investment_leads.models import InvestmentRequirement
from requirements.models import Requirement
from .models import SiteConfig, ContactForm, Developer


def home(request):
    """Home page view"""
    # Get categories with featured projects
    categories = Category.objects.all()
    cities = City.objects.filter(is_active=True)
    
    # Get project types for filters
    residential_types = ProjectType.objects.filter(category__name__icontains='residential')
    commercial_types = ProjectType.objects.filter(category__name__icontains='commercial')
    amenities = Amenity.objects.filter(is_active=True)[:8]  # Show first 8 amenities
    
    # Featured projects
    featured_projects = Project.objects.filter(
        is_featured=True, 
        is_active=True
    ).select_related('city', 'category', 'project_type').prefetch_related('amenities')[:6]
    
    # Add featured projects to categories
    for category in categories:
        category.featured_projects = Project.objects.filter(
            category=category,
            is_active=True
        ).select_related('city', 'project_type').prefetch_related('amenities')[:6]
    
    # Trending properties (most viewed)
    trending_projects = Project.objects.filter(
        is_active=True
    ).order_by('-views')[:8]
    
    # Ready to move properties
    ready_to_move_projects = Project.objects.filter(
        status='ready_to_move',
        is_active=True
    ).select_related('city', 'project_type').prefetch_related('amenities')[:8]
    
    # Recently Viewed Properties (can be based on session or default to newest)
    recently_viewed_projects = Project.objects.filter(
        is_active=True
    ).order_by('-created_at')[:8]
    
    # Hot Deals
    hot_deal_projects = Project.objects.filter(
        is_hot_deal=True,
        is_active=True
    ).select_related('city', 'project_type').prefetch_related('amenities')[:8]
    
    # Premium Listings
    premium_projects = Project.objects.filter(
        is_premium_listing=True,
        is_active=True
    ).select_related('city', 'project_type').prefetch_related('amenities')[:8]
    
    # Editor's Choice
    editors_choice_projects = Project.objects.filter(
        is_editors_choice=True,
        is_active=True
    ).select_related('city', 'project_type').prefetch_related('amenities')[:8]
    
    # Projects by Category for horizontal scrolling
    residential_projects = Project.objects.filter(
        category__name__icontains='residential',
        is_active=True
    ).select_related('city', 'project_type').prefetch_related('amenities')[:10]
    
    commercial_projects = Project.objects.filter(
        category__name__icontains='commercial',
        is_active=True
    ).select_related('city', 'project_type').prefetch_related('amenities')[:10]
    
    # Active developers for the developers section
    active_developers = Developer.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'categories': categories,
        'cities': cities,
        'residential_types': residential_types,
        'commercial_types': commercial_types,
        'amenities': amenities,
        'featured_projects': featured_projects,
        'trending_projects': trending_projects,
        'ready_to_move_projects': ready_to_move_projects,
        'recently_viewed_projects': recently_viewed_projects,
        'hot_deal_projects': hot_deal_projects,
        'premium_projects': premium_projects,
        'editors_choice_projects': editors_choice_projects,
        'residential_projects': residential_projects,
        'commercial_projects': commercial_projects,
        'active_developers': active_developers,
    }
    
    return render(request, 'pages/home.html', context)


def search_properties(request):
    """Search and filter properties"""
    # Get all projects
    projects = Project.objects.filter(is_active=True).select_related(
        'city', 'category', 'project_type'
    ).prefetch_related('amenities')
    
    # Get filter options
    categories = Category.objects.all()
    cities = City.objects.filter(is_active=True)
    project_types = ProjectType.objects.all()
    amenities = Amenity.objects.filter(is_active=True)
    
    # Store applied filters for display
    applied_filters = []
    
    # Apply filters
    search_query = request.GET.get('q')
    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query) |
            Q(project_by__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(developers__icontains=search_query)
        )
        applied_filters.append({
            'label': 'Search',
            'value': search_query,
            'param': 'q',
            'raw_value': search_query
        })
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        try:
            # Try to get by ID first
            if category_id.isdigit():
                category = Category.objects.get(id=category_id)
            else:
                # Try to get by name if not a digit
                category = Category.objects.get(name__iexact=category_id)
            projects = projects.filter(category=category)
            applied_filters.append({
                'label': 'Category',
                'value': category.name,
                'param': 'category',
                'raw_value': category_id
            })
        except (Category.DoesNotExist, ValueError):
            pass
    
    # City filter
    city_id = request.GET.get('city')
    if city_id:
        try:
            # Try to get by ID first
            if city_id.isdigit():
                city = City.objects.get(id=city_id)
            else:
                # Try to get by name if not a digit
                city = City.objects.get(name__iexact=city_id)
            projects = projects.filter(city=city)
            applied_filters.append({
                'label': 'City',
                'value': city.name,
                'param': 'city',
                'raw_value': city_id
            })
        except (City.DoesNotExist, ValueError):
            pass
    
    # Project type filter
    project_type_id = request.GET.get('project_type')
    if project_type_id:
        try:
            # Try to get by ID first
            if project_type_id.isdigit():
                project_type = ProjectType.objects.get(id=project_type_id)
            else:
                # Try to get by name if not a digit
                project_type = ProjectType.objects.get(name__iexact=project_type_id)
            projects = projects.filter(project_type=project_type)
            applied_filters.append({
                'label': 'Type',
                'value': project_type.name,
                'param': 'project_type',
                'raw_value': project_type_id
            })
        except (ProjectType.DoesNotExist, ValueError):
            pass
    
    # BHK filter
    bhk = request.GET.get('bhk')
    if bhk:
        if bhk == '4':
            projects = projects.filter(bhk__icontains='4')
        else:
            projects = projects.filter(bhk__icontains=f'{bhk} BHK')
        applied_filters.append({
            'label': 'BHK',
            'value': f'{bhk}{"+" if bhk == "4" else ""} BHK',
            'param': 'bhk',
            'raw_value': bhk
        })
    
    # Budget filter
    budget = request.GET.get('budget')
    if budget:
        budget_labels = {
            '0-2000000': 'Under ₹20L',
            '2000000-5000000': '₹20L - ₹50L',
            '5000000-10000000': '₹50L - ₹1Cr',
            '10000000-20000000': '₹1Cr - ₹2Cr',
            '20000000-50000000': '₹2Cr - ₹5Cr',
            '50000000-': '₹5Cr+',
        }
        
        if '-' in budget:
            min_price, max_price = budget.split('-')
            if min_price:
                projects = projects.filter(onwards_price__gte=int(min_price))
            if max_price:
                projects = projects.filter(onwards_price__lte=int(max_price))
        
        applied_filters.append({
            'label': 'Budget',
            'value': budget_labels.get(budget, budget),
            'param': 'budget',
            'raw_value': budget
        })
    
    # Status filter
    status = request.GET.get('status')
    if status:
        projects = projects.filter(status=status)
        status_labels = {
            'ready_to_move': 'Ready to Move',
            'under_construction': 'Under Construction',
            'upcoming': 'Upcoming',
            'sold_out': 'Sold Out'
        }
        applied_filters.append({
            'label': 'Status',
            'value': status_labels.get(status, status),
            'param': 'status',
            'raw_value': status
        })
    
    # Amenities filter
    amenity_ids = request.GET.getlist('amenities')
    if amenity_ids:
        projects = projects.filter(amenities__id__in=amenity_ids).distinct()
        selected_amenities = Amenity.objects.filter(id__in=amenity_ids)
        for amenity in selected_amenities:
            applied_filters.append({
                'label': 'Amenity',
                'value': amenity.name,
                'param': 'amenities',
                'raw_value': str(amenity.id)
            })
    
    # Special filters
    if request.GET.get('featured'):
        projects = projects.filter(is_featured=True)
        applied_filters.append({
            'label': 'Filter',
            'value': 'Featured',
            'param': 'featured',
            'raw_value': 'true'
        })
    
    if request.GET.get('trending'):
        projects = projects.filter(trending_tag__isnull=False)
        applied_filters.append({
            'label': 'Filter',
            'value': 'Trending',
            'param': 'trending',
            'raw_value': 'true'
        })
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'onwards_price', '-onwards_price', '-views', 'name']
    if sort_by in valid_sorts:
        projects = projects.order_by(sort_by)
    else:
        projects = projects.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(projects, 16)  # Show 16 projects per page (4x4 grid)
    page_number = request.GET.get('page')
    projects_page = paginator.get_page(page_number)
    
    context = {
        'projects': projects_page,
        'categories': categories,
        'cities': cities,
        'project_types': project_types,
        'amenities': amenities,
        'applied_filters': applied_filters,
    }
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'pages/search_properties_ajax.html', context)
    
    return render(request, 'pages/search_properties.html', context)


def project_detail(request, project_id):
    """Redirect to the new Projects app project detail view"""
    from django.shortcuts import redirect
    
    # Redirect to the Projects app public project detail view
    return redirect('public_project_detail', project_id=project_id)


@require_POST
def increment_project_views(request, project_id):
    """Increment project view count"""
    try:
        project = Project.objects.get(id=project_id, is_active=True)
        project.increment_views()
        return JsonResponse({'success': True, 'views': project.views})
    except Project.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found'})


@require_POST
def land_requirement(request):
    """Handle land requirement form submission"""
    try:
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'contact_number': request.POST.get('contact_number'),
            'location': request.POST.get('location'),
            'budget': request.POST.get('budget'),
            'area': request.POST.get('area'),
            'area_unit': request.POST.get('area_unit'),
            'requirement_type': request.POST.get('requirement_type'),
            'agreed_to_terms': request.POST.get('agreed_to_terms') == 'on',
        }
        
        # Validate required fields
        if not data['name'] or not data['contact_number'] or not data['requirement_type']:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('theme:home')
        
        # Create land requirement
        land_req = LandRequirement.objects.create(**data)
        
        messages.success(request, 'Thank you! Your land requirement has been submitted successfully. We will contact you soon.')
        return redirect('theme:home')
        
    except Exception as e:
        messages.error(request, 'Sorry, there was an error submitting your requirement. Please try again.')
        return redirect('theme:home')


@require_POST
def investment_requirement(request):
    """Handle investment requirement form submission"""
    try:
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'contact_number': request.POST.get('contact_number'),
            'location': request.POST.get('location'),
            'budget': request.POST.get('budget'),
            'requirement_type': request.POST.get('requirement_type'),
            'how_did_you_know': request.POST.get('how_did_you_know'),
            'agreed_to_terms': request.POST.get('agreed_to_terms') == 'on',
        }
        
        # Validate required fields
        if not data['name'] or not data['contact_number'] or not data['budget'] or not data['requirement_type']:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('theme:investment_page')
        
        # Create investment requirement
        investment_req = InvestmentRequirement.objects.create(**data)
        
        messages.success(request, 'Thank you! Your investment inquiry has been submitted successfully. We will contact you soon.')
        return redirect('theme:investment_page')
        
    except Exception as e:
        messages.error(request, 'Sorry, there was an error submitting your inquiry. Please try again.')
        return redirect('theme:investment_page')


def land_page(request):
    """Land page view with form"""
    from .models import SiteConfig
    
    # Get site configuration for contact information
    site_config = SiteConfig.get_config()
    
    context = {
        'page_title': 'Land Requirements',
        'area_units': LandRequirement.AREA_UNIT_CHOICES,
        'requirement_types': LandRequirement.REQUIREMENT_TYPE_CHOICES,
        'site_config': site_config,
    }
    return render(request, 'pages/land.html', context)


def requirements_page(request):
    """Requirements page view with form"""
    from .models import SiteConfig
    from requirements.models import Requirement
    
    # Get site configuration for contact information
    site_config = SiteConfig.get_config()
    
    context = {
        'page_title': 'Property Requirements',
        'requirement_types': Requirement.REQUIREMENT_TYPE_CHOICES,
        'property_types': Requirement.PROPERTY_TYPE_CHOICES,
        'budget_ranges': Requirement.BUDGET_RANGE_CHOICES,
        'site_config': site_config,
    }
    return render(request, 'pages/requirements.html', context)


def requirements_submission(request):
    """Handle requirements form submission"""
    from requirements.models import Requirement
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            contact_number = request.POST.get('contact_number')
            email = request.POST.get('email', '')
            location = request.POST.get('location', '')
            budget = request.POST.get('budget')
            budget_range = request.POST.get('budget_range', '')
            requirement_type = request.POST.get('requirement_type')
            property_type = request.POST.get('property_type')
            area_needed = request.POST.get('area_needed', '')
            specific_requirements = request.POST.get('specific_requirements', '')
            agreed_to_terms = request.POST.get('agreed_to_terms') == 'on'
            
            # Create requirement
            requirement = Requirement.objects.create(
                name=name,
                contact_number=contact_number,
                email=email,
                location=location,
                budget=budget,
                budget_range=budget_range,
                requirement_type=requirement_type,
                property_type=property_type,
                area_needed=area_needed,
                specific_requirements=specific_requirements,
                agreed_to_terms=agreed_to_terms
            )
            
            messages.success(request, 'Your property requirement has been submitted successfully! Our team will contact you soon.')
            return redirect('theme:requirements_page')
            
        except Exception as e:
            messages.error(request, 'Sorry, there was an error submitting your requirement. Please try again.')
            return redirect('theme:requirements_page')
    
    return redirect('theme:requirements_page')


def investment_page(request):
    """Investment page view with form - Updated for investment opportunities"""
    from .models import SiteConfig
    
    # Get site configuration for contact information
    site_config = SiteConfig.get_config()
    
    context = {
        'page_title': 'Investment Opportunities',
        'requirement_types': InvestmentRequirement.REQUIREMENT_TYPE_CHOICES,
        'how_did_you_know_choices': InvestmentRequirement.HOW_DID_YOU_KNOW_CHOICES,
        'site_config': site_config,
    }
    return render(request, 'pages/investment.html', context)


def contact_us(request):
    """Contact Us page view"""
    if request.method == 'POST':
        # Handle contact form submission
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            # Save to database
            contact_submission = ContactForm.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('theme:contact_us')
            
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
    
    # Get site config (singleton)
    site_config = SiteConfig.get_config()
    context = {
        'page_title': 'Contact Us',
        'site_config': site_config,
    }
    return render(request, 'pages/contact_us.html', context)


@csrf_exempt
def ajax_project_types(request):
    """AJAX endpoint to get project types by category"""
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        if category_id:
            project_types = ProjectType.objects.filter(category_id=category_id).values('id', 'name')
            return JsonResponse({'project_types': list(project_types)})
    return JsonResponse({'project_types': []})
