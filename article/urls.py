from django.urls import path
from .views import CourseListView, CourseDetailView, HomeView




app_name = "courses"

urlpatterns = [
    path('', HomeView.as_view(), name='home' ),
    path("courses/" , CourseListView.as_view(), name="course-list"),
    path("courses/<slug:slug>/" , CourseDetailView.as_view(), name="course-detail"),
]