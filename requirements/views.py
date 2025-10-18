from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Requirement


def requirement_submission(request):
    """Handle requirement form submission"""
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
