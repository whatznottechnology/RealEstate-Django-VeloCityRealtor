from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import LandRequirement


@staff_member_required
def land_requirement_detail_view(request, requirement_id):
    """Detailed view of a land requirement for admin users"""
    requirement = get_object_or_404(LandRequirement, id=requirement_id)
    
    # Get admin context for sidebar navigation
    from django.contrib.admin import site
    admin_context = site.each_context(request)
    
    context = {
        'requirement': requirement,
        'title': f'Land Requirement Details - {requirement.name}',
    }
    
    # Add admin context for sidebar navigation
    context.update(admin_context)
    
    return render(request, 'admin/land_leads/requirement_detail.html', context)
