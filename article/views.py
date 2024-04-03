from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView,TemplateView
from django.utils.translation import gettext_lazy as _
from view_breadcrumbs import DetailBreadcrumbMixin , BaseBreadcrumbMixin
from .models import Course, Videos


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
    # def get_queryset(self):
    #     if self.request.method == 'GET':
    #         queryset = get_object_or_404(Course, slug = self.kwargs["slug"]) 
    #         return queryset


class VideoDetailView(DetailView):

    template_name = "article/course_detail.html"
    model = Course
    
    def get_object(self):
        # return get_object_or_404(Videos, id=self.kwargs["pk"])
        global  course_query 
        course_query   = get_object_or_404(Course, slug=self.kwargs["slug"]) #course_slug
        return course_query 
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pk = self.kwargs.get("pk", None)
        if  pk :
            # context['video_file'] = get_object_or_404(Videos,pk = self.kwargs["pk"], slug=self.kwargs["video_slug"]  ).videofile
            # Videos.objects.select_related("course").get(pk = self.kwargs["pk"], slug=self.kwargs["video_slug"]).videofile
            video_query = course_query.videos.get(pk = self.kwargs["pk"], slug=self.kwargs["video_slug"])
            context['video_title'] = video_query.title
            context['video_is_free'] = video_query.is_free
            if  video_query.is_free:
                context['video_file'] =  video_query.videofile
            context['video_description'] = video_query.video_description
        return context
