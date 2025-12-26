from django.shortcuts import render, get_object_or_404
from .models import Blogs

def blog_list(request):
    blogs = Blogs.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'blogs': blogs})


def blog_detail(request, slug):
    blog = get_object_or_404(Blogs, slug=slug, is_active=True)
    return render(request, 'blog/blog_detail.html', {'blog': blog})
