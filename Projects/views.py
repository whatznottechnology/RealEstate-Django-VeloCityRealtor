from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Project, Category, ProjectType, GalleryImage, FloorPlan
from .forms import ProjectForm
from theme.models import SiteConfig


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

    return render(request, 'pages/project_detail.html', context)


def public_project_detail_view(request, project_id):
    """Public detailed view of a project using the new template"""
    project = get_object_or_404(Project, id=project_id, is_active=True)
    
    # Increment view count
    project.increment_views()
    
    # Get site configuration
    site_config = SiteConfig.get_config()
    
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
        'construction_updates': project.construction_updates.all().order_by('order'),
        'why_choose_us': project.why_choose_us.all().order_by('order'),
        'specifications': project.specifications.all().order_by('category__name', 'order'),
        'amenity_images': project.amenity_images.filter(is_active=True),
        'project_overview': getattr(project, 'overview', None),
        'site_config': site_config,
        'related_projects': related_projects,
        'title': f'{project.name} - Project Details',
    }

    return render(request, 'pages/project_detail_final.html', context)


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
