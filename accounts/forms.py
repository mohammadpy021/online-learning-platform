from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseRedirect
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
class SignupForm(UserCreationForm):
    # email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    ## in case of auto Login
    # def form_valid(self, form):
    #     #save the new user first
    #     form.save()
    #     #get the username and password
    #     username = self.request.POST['username']
    #     password = self.request.POST['password1']
    #     #authenticate user then login
    #     user = authenticate(username=username, password=password)
    #     login(self.request, user)
    #     return HttpResponseRedirect(self.get_success_url)
        


class UserForm(forms.ModelForm): # class UserForm(UserChangeForm):   

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


        
        if not self.user.is_superuser :
            # self.fields['date_joined'].required = False
            # self.fields['date_joined'].widget.attrs['readonly'] = True
            self.fields['date_joined'].disabled = True
            self.fields['last_login'].disabled = True
            self.fields['email'].disabled = True 
           
    # def clean_email(self):
    ''' this will stop malicious Post same as ".disabled "'''
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         return instance.email
    #     else:
    #         return self.cleaned_data['email']     

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'date_joined', 'username', 'email', 'last_login')
