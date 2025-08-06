from django.shortcuts import render, get_object_or_404
from .models import Blog

def blog_list(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blogs/blog_list.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    return render(request, 'blogs/blog_detail.html', {'blog': blog})
