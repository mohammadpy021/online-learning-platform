from django.urls import path
from .views import (CourseListView, CourseDetailView, HomeView, VideoDetailView,
                    # QuizView,
                    quiz_view
)



app_name = "courses"

urlpatterns = [
    path('', HomeView.as_view(), name='home' ),
    path("courses/" , CourseListView.as_view(), name="course-list"),
    path("courses/quiz/<int:quiz_id>/" , quiz_view, name="quiz"),
    # path("courses/quiz/<int:quiz_id>/" , QuizView.as_view(), name="quiz"),
    path("courses/<slug:slug>/" , CourseDetailView.as_view(), name="course-detail"),
    path("courses/<slug:slug>/episode/<int:pk>/<slug:video_slug>/" , VideoDetailView.as_view(), name="video-detail"),
    
    # path("courses/episode/<int:pk>/" , VideoDetailView.as_view(), name="video-detail"),
]