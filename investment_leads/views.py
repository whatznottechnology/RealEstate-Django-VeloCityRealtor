from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import InvestmentRequirement


@staff_member_required
def investment_requirement_detail_view(request, requirement_id):
    """Detailed view of an investment requirement for admin users"""
    requirement = get_object_or_404(InvestmentRequirement, id=requirement_id)
    
    # Get admin context for sidebar navigation
    from django.contrib.admin import site
    admin_context = site.each_context(request)
    
    context = {
        'requirement': requirement,
        'title': f'Investment Requirement Details - {requirement.name}',
    }
    
    # Add admin context for sidebar navigation
    context.update(admin_context)
    
    return render(request, 'admin/investment_leads/requirement_detail.html', context)
