from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView,TemplateView
from django.utils.translation import gettext_lazy as _
from view_breadcrumbs import DetailBreadcrumbMixin , BaseBreadcrumbMixin
from .models import Course


class HomeView(TemplateView):
    template_name = 'article/index.html'
    #TODO:
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['blogs'] = Blog.objects.all()[0:3]
    #     return context


class CourseListView(ListView):
    
    queryset = Course.objects.active()
    #TODO paginate_by = 3 
    context_object_name = "courses"


class CourseDetailView(DetailView):
    model = Course

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['blogs'] = Blog.objects.all()[0:3]
    #     return context


