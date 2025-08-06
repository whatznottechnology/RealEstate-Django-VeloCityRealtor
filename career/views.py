from django.shortcuts import render, get_object_or_404, redirect
from .models import Career
from .forms import CareerApplicationForm

def career_list(request):
    careers = Career.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'career/career_list.html', {'careers': careers})

def career_detail(request, slug):
    career = get_object_or_404(Career, slug=slug, is_active=True)
    if request.method == 'POST':
        form = CareerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.career = career
            application.save()
            return render(request, 'career/application_success.html', {'career': career})
    else:
        form = CareerApplicationForm()
    return render(request, 'career/career_detail.html', {'career': career, 'form': form})
