from django.shortcuts import render
from . import models

# Create your views here.
def blogSidebarList(self):
    blogpages = models.BlogPage.objects.all().order_by('-first_published_at')[:3]
    # Update template context
    context = {
        "blog_sidebar_list": blogpages,
    }
    return context

def blogHomePageList(self):
    blogpages = models.BlogPage.objects.all().order_by('-first_published_at')[:3]
    # Update template context
    context = {
        "home_blog_list": blogpages,
    }
    return context

# def blog_sidebar_list(self):
#     sidebarBlogs = models.BlogPage.objects.all()
#     sidebarBlogs = sidebarBlogs.order_by('-first_published_at')[:2]
#     print(sidebarBlogs)
#     return sidebarBlogs
