from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import RedirectAuthenticatedMixin
from .forms import SignupForm, UserForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView


class SignUpView(RedirectAuthenticatedMixin, CreateView): #RedirectURLMixin
    template_name = "registration/signup.html"
    redirect_authenticated_user = True
    form_class = SignupForm

    # success_url = reverse_lazy('accounts:login')
    def get_success_url(self):
        messages.success(self.request, 'حساب شما با موفقیت ایجاد شد، لطفا اکنون وارد شوید')
        return self.request.GET.get('next', reverse(settings.LOGIN_URL))
    

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

    
class HomeView(LoginRequiredMixin, TemplateView ):
    template_name = "registration/home.html"

class CustomPasswordChangeView(PasswordChangeView):

    def get_success_url(self):
        messages.success(self.request, 'پسورد شما با موفقیت تغییر پیدا کرد')
        return reverse("accounts:profile")
