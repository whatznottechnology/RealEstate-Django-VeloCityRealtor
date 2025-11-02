from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Project, Category, ProjectType, GalleryImage, FloorPlan, FloorPlanAccess, ProjectInquiry
from .forms import ProjectForm
from theme.models import SiteConfig
import json


def index(request):
    """Index view for projects"""
    return render(request, 'projects/index.html')


@staff_member_required
def project_detail_view(request, project_id):
    """Detailed view of a project for admin users"""
    project = get_object_or_404(Project, id=project_id)
    
    context = {
        'project': project,
        'gallery_images': project.gallery_images.filter(is_active=True).order_by('order'),
        'floor_plans': project.floor_plans.filter(is_active=True).order_by('order'),
        'nearest_areas': project.nearest_areas.all().order_by('area_type', 'name'),
        'construction_updates': project.construction_updates.all().order_by('order'),
        'why_choose_us': project.why_choose_us.all().order_by('order'),
        'specifications': project.specifications.all().order_by('category__name', 'order'),
        'amenity_images': project.amenity_images.filter(is_active=True),
        'project_overview': getattr(project, 'overview', None),
        'title': f'Project Details - {project.name}',
    }

    return render(request, 'admin/Projects/project_detail.html', context)


def public_project_detail_view(request, project_id):
    """Public detailed view of a project using the new redesigned template"""
    from datetime import date
    
    project = get_object_or_404(Project, id=project_id, is_active=True)
    
    # Increment view count
    project.increment_views()
    
    # Get site configuration
    site_config = SiteConfig.get_config()
    
    # Check if user has floor plan access (using session-based tracking)
    session_key = f'floor_plan_access_{project_id}'
    has_floor_plan_access = request.session.get(session_key, False)
    
    # Get related projects (same category or city)
    related_projects = Project.objects.filter(
        is_active=True
    ).exclude(id=project.id)
    
    if project.category:
        related_projects = related_projects.filter(category=project.category)
    elif project.city:
        related_projects = related_projects.filter(city=project.city)
    
    related_projects = related_projects[:4]
    
    context = {
        'project': project,
        'gallery_images': project.gallery_images.filter(is_active=True).order_by('order'),
        'floor_plans': project.floor_plans.filter(is_active=True).order_by('order'),
        'nearest_areas': project.nearest_areas.all().order_by('area_type', 'name'),
        'construction_updates': project.construction_updates.all().order_by('-update_date', 'order'),
        'why_choose_us': project.why_choose_us.all().order_by('order'),
        'specifications': project.specifications.all().order_by('category__order', 'order'),
        'amenity_images': project.amenity_images.filter(is_active=True),
        'project_overview': getattr(project, 'overview', None),
        'site_config': site_config,
        'related_projects': related_projects,
        'has_floor_plan_access': has_floor_plan_access,
        'today_date': date.today(),  # For date input min attribute
        'title': f'{project.name} - Project Details',
    }

    return render(request, 'pages/project_detail_redesign.html', context)


def project_create(request):
    """Create a new project with single-page form"""
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            
            # Handle gallery images
            gallery_images = request.FILES.getlist('gallery_images')
            for i, image in enumerate(gallery_images):
                GalleryImage.objects.create(
                    project=project,
                    image=image,
                    order=i + 1,
                    is_active=True
                )
            
            # Handle floor plan images
            floor_plan_images = request.FILES.getlist('floor_plan_images')
            for i, image in enumerate(floor_plan_images):
                FloorPlan.objects.create(
                    project=project,
                    image=image,
                    order=i + 1,
                    is_active=True
                )
            
            messages.success(request, f'Project "{project.name}" has been created successfully!')
            return redirect('admin:Projects_project_change', project.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm()
    
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Create New Project'})


def project_edit(request, project_id):
    """Edit an existing project"""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            
            # Handle gallery images (append new ones)
            gallery_images = request.FILES.getlist('gallery_images')
            if gallery_images:
                existing_count = GalleryImage.objects.filter(project=project).count()
                for i, image in enumerate(gallery_images):
                    GalleryImage.objects.create(
                        project=project,
                        image=image,
                        order=existing_count + i + 1,
                        is_active=True
                    )
            
            # Handle floor plan images (append new ones)
            floor_plan_images = request.FILES.getlist('floor_plan_images')
            if floor_plan_images:
                existing_count = FloorPlan.objects.filter(project=project).count()
                for i, image in enumerate(floor_plan_images):
                    FloorPlan.objects.create(
                        project=project,
                        image=image,
                        order=existing_count + i + 1,
                        is_active=True
                    )
            
            messages.success(request, f'Project "{project.name}" has been updated successfully!')
            return redirect('admin:Projects_project_change', project.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-populate form with existing data
        initial_data = {}
        
        # Get project overview data
        if hasattr(project, 'overview'):
            initial_data['overview_title'] = project.overview.title
            initial_data['overview_description'] = project.overview.short_description
        
        # Get nearest areas
        nearest_areas = project.nearest_areas.all().order_by('order')
        if nearest_areas:
            areas_list = [f"{area.place} - {area.distance}" for area in nearest_areas]
            initial_data['nearest_areas'] = ', '.join(areas_list)
        
        # Get construction updates
        construction_updates = project.construction_updates.all().order_by('order')
        if construction_updates:
            updates_list = [update.update for update in construction_updates]
            initial_data['construction_updates'] = ', '.join(updates_list)
        
        # Get why choose us points
        why_choose_us = project.why_choose_us.all().order_by('order')
        if why_choose_us:
            points_list = [point.point for point in why_choose_us]
            initial_data['why_choose_us'] = ', '.join(points_list)
        
        form = ProjectForm(instance=project, initial=initial_data)
    
    return render(request, 'projects/project_form.html', {
        'form': form, 
        'project': project,
        'title': f'Edit Project: {project.name}'
    })


def get_project_types(request):
    """AJAX endpoint to get project types based on category"""
    category_id = request.GET.get('category_id')
    if category_id:
        project_types = ProjectType.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse({'project_types': list(project_types)})
    return JsonResponse({'project_types': []})


@csrf_exempt
@require_POST
def increment_project_views(request, project_id):
    """AJAX endpoint to increment project views"""
    try:
        project = get_object_or_404(Project, id=project_id, is_active=True)
        project.increment_views()
        return JsonResponse({'success': True, 'views': project.views})
    except:
        return JsonResponse({'success': False})


@csrf_exempt
@require_POST
def submit_floor_plan_access(request, project_id):
    """Submit contact details to access floor plans"""
    try:
        project = get_object_or_404(Project, id=project_id, is_active=True)
        
        # Get form data
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()
        
        # Validate required fields
        if not name or not email or not phone:
            return JsonResponse({
                'success': False, 
                'error': 'Name, email, and phone are required fields.'
            })
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False, 
                'error': 'Please enter a valid email address.'
            })
        
        # Validate phone (basic check)
        if len(phone) < 10:
            return JsonResponse({
                'success': False, 
                'error': 'Please enter a valid phone number.'
            })
        
        # Get IP address and user agent
        ip_address = request.META.get('REMOTE_ADDR')
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0].strip()
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Create floor plan access record
        FloorPlanAccess.objects.create(
            project=project,
            name=name,
            email=email,
            phone=phone,
            message=message,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Grant access in session
        session_key = f'floor_plan_access_{project_id}'
        request.session[session_key] = True
        request.session.modified = True
        
        return JsonResponse({
            'success': True, 
            'message': 'Thank you! You can now view the floor plans.'
        })
        
    except json.JSONDecodeError as e:
        return JsonResponse({
            'success': False, 
            'error': f'Invalid JSON format: {str(e)}'
        }, status=400)
    except Project.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'error': 'Project not found.'
        }, status=404)
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return JsonResponse({
            'success': False, 
            'error': f'Server error: {error_msg}'
        }, status=500)


@csrf_exempt
@require_POST
def submit_project_inquiry(request, project_id):
    """Submit project inquiry form"""
    try:
        project = get_object_or_404(Project, id=project_id, is_active=True)
        
        # Get form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
            
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        interest = data.get('interest', '').strip()
        message = data.get('message', '').strip()
        appointment_date = data.get('appointment_date', '').strip()
        appointment_time = data.get('appointment_time', '').strip()
        
        # Validate required fields
        if not name or not email or not phone:
            return JsonResponse({
                'success': False, 
                'error': 'Name, email, and phone are required fields.'
            })
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False, 
                'error': 'Please enter a valid email address.'
            })
        
        # Validate phone (basic check)
        if len(phone) < 10:
            return JsonResponse({
                'success': False, 
                'error': 'Please enter a valid phone number.'
            })
        
        # Validate appointment fields if site visit is selected
        if interest == 'site_visit' and (not appointment_date or not appointment_time):
            return JsonResponse({
                'success': False,
                'error': 'Please select both date and time for site visit.'
            })
        
        # Get IP address and user agent
        ip_address = request.META.get('REMOTE_ADDR')
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0].strip()
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Create inquiry record
        inquiry = ProjectInquiry.objects.create(
            project=project,
            name=name,
            email=email,
            phone=phone,
            interest=interest if interest else None,
            message=message,
            appointment_date=appointment_date if appointment_date else None,
            appointment_time=appointment_time if appointment_time else None,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Customize success message based on inquiry type
        if appointment_date and appointment_time:
            success_message = f'Thank you! Your site visit has been scheduled for {appointment_date} at {appointment_time}. We will contact you to confirm.'
        else:
            success_message = 'Thank you for your inquiry! We will contact you within 24 hours.'
        
        return JsonResponse({
            'success': True, 
            'message': success_message
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'error': 'Invalid request format.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred. Please try again.'
        })
