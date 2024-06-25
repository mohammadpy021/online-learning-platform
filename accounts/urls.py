from django.urls import path
from django.contrib.auth import views
from .views import SignUpView, ProfileView, HomeView, CustomPasswordChangeView, CustomLogoutView, add_course_view
app_name = "accounts"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("add-course/", add_course_view, name="add-course"),
    path("login/", views.LoginView.as_view(redirect_authenticated_user = True), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"), 
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "password_change/", CustomPasswordChangeView.as_view(), name="password_change"
    ),
    # path(
    #     "password_change/done/",
    #     views.PasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
    # path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    # path(
    #     "password_reset/done/",
    #     views.PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     views.PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "reset/done/",
    #     views.PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
]



