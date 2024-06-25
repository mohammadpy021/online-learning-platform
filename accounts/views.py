from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView, TemplateView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from article.models import Course
from .mixins import RedirectAuthenticatedMixin
from .forms import SignupForm, UserForm

class SignUpView(RedirectAuthenticatedMixin, CreateView): #RedirectURLMixin
    template_name = "registration/signup.html"
    redirect_authenticated_user = True
    form_class = SignupForm

    # success_url = reverse_lazy('accounts:login')
    def get_success_url(self):
        # messages.success(self.request, 'حساب شما با موفقیت ایجاد شد، لطفا اکنون وارد شوید')
        # return self.request.GET.get('next', reverse("accounts:login"))
        return self.request.GET.get('next', reverse("courses:home"))
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get('next')
        return context

    
    ## in case of auto Login
    def form_valid(self, form):
        # save the new user first
        form.save()
        # user = form.save(commit=False)
        # user.set_password(form.cleaned_data.get("password1"))
        # user.save()
        
        # get the username and password
        # username = self.request.POST['username']
        email  = form.cleaned_data['email']
        password =  form.cleaned_data['password1']
        # authenticate user then login
        user = authenticate(email=email, password=password)
        login(self.request, user)
        # return HttpResponseRedirect(self.request.GET.get('next', reverse("courses:home")))
        next_page = self.request.GET.get('next')
        if next_page is None or next_page == '':
            next_page = reverse("courses:home")
        return redirect(next_page)
    
    

class ProfileView(LoginRequiredMixin, UpdateView): #RedirectURLMixin
    template_name = "registration/profile.html"
    # form_class = UserForm
    model = get_user_model()
    fields = ('first_name', 'last_name', 'date_joined', 'username', 'email', 'last_login')
    success_url = reverse_lazy('accounts:home')

    def get_object(self):
        return get_object_or_404(get_user_model(), id=self.request.user.id)
        
    def get_form(self, form_class=None):#we can also send "user" via "get_form_kwargs" to the form

        # self.fields = ('username',)
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Disable these fields
            form.fields["date_joined"].disabled = True
            form.fields["last_login"].disabled = True
            form.fields["email"].disabled = True
       
        return form
    
    # def get_form_kwargs(self):
    #     """Return the keyword arguments for instantiating the form."""
    #     kwargs = super().get_form_kwargs()
    #     if hasattr(self, "object"):
    #         kwargs['user'] = self.request.user
    #     return kwargs

    
class HomeView(LoginRequiredMixin, ListView ):
    template_name = "registration/home.html"
    context_object_name = "courses"
    def get_queryset(self):
        return self.request.user.courses.all()
    

class CustomPasswordChangeView(PasswordChangeView):

    def get_success_url(self):
        messages.success(self.request, 'پسورد شما با موفقیت تغییر پیدا کرد')
        return reverse("accounts:profile")
    

class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return self.request.GET.get('next', reverse("courses:home"))

# class CustomLoginView(LoginView):
#     def get_success_url(self):
#         return self.request.GET.get('next', reverse("courses:home"))


def add_course_view(request):
    if request.method == 'POST' and request.user.is_authenticated :
        course_id = request.POST.get("course_id")
        course_slug = request.POST.get("course_slug")
        if course_id and course_slug:
            request.user.courses.add(Course.objects.get(id=course_id))
            return redirect(reverse("courses:course-detail", kwargs={"slug" : course_slug}))
    
    return redirect(reverse("courses:home"))

