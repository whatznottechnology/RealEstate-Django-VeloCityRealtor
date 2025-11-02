from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import InteriorInquiry, InteriorService, PortfolioWork
from .forms import InteriorInquiryForm
from theme.models import SiteConfig, Testimonial

def interior_page(request):
    """Interior services page with inquiry form"""
    if request.method == 'POST':
        form = InteriorInquiryForm(request.POST)
        
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if form.is_valid():
            inquiry = form.save()
            
            if is_ajax:
                # Return JSON response for AJAX
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your interest! We will contact you within 24 hours.'
                })
            else:
                # Traditional form submission with redirect
                messages.success(
                    request, 
                    'Thank you for your interest! We will contact you within 24 hours.'
                )
                return redirect('interior:interior_page')
        else:
            if is_ajax:
                # Return JSON response with errors
                errors = []
                for field, error_list in form.errors.items():
                    for error in error_list:
                        errors.append(f"{field}: {error}")
                return JsonResponse({
                    'success': False,
                    'message': ' '.join(errors)
                }, status=400)
            else:
                # Traditional form submission with error message
                messages.error(
                    request,
                    'Please correct the errors below.'
                )
    else:
        form = InteriorInquiryForm()
    
    # Get site configuration from theme app
    site_config = SiteConfig.get_config()
    
    # Get active services and portfolio works
    services = InteriorService.objects.filter(is_active=True)
    portfolio_works = PortfolioWork.objects.filter(is_active=True)[:6]  # Show 6 recent works
    
    # Get active testimonials (featured first, then by display order)
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    context = {
        'form': form,
        'site_config': site_config,
        'services': services,
        'portfolio_works': portfolio_works,
        'testimonials': testimonials,
    }
    return render(request, 'interior/interior.html', context)

def submit_inquiry_ajax(request):
    """AJAX endpoint for form submission"""
    if request.method == 'POST':
        form = InteriorInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your interest! We will contact you within 24 hours.'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

