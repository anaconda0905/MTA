from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models as db_models
from .models import Profile

# forms.py
class UserProfileForm(forms.ModelForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = User
        # fields = ('first_name', 'last_name', 'email')
        fields = ('username','email',)

class ProfileForm(forms.ModelForm):
    fullname = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control'}), max_length=254, required=True,label="Full Name as NRIC")
    nric = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control'}), max_length=254, required=False, label="NRIC")
    birth_date = forms.DateField(
        required=False,
        label = "Date Of Birth",
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )
    
    image = forms.ImageField(required=False,widget= forms.FileInput(attrs={'class': 'form-control', }))
    phone = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'(xxx)xxx-xxxx', 'class': 'form-control'}), label="MOBILE NO.", required=False)

    class Meta:
        model = Profile
        fields = ('fullname','nric', 'birth_date', 'phone', 'image')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['style'] = 'class: form-control;'
        
class SignUpForm(UserCreationForm):
    # fullname = forms.CharField(max_length=254, required=True,label="Full Name as NRIC")
    # nric = forms.CharField(max_length=254, required=False, label="NRIC")
    # birth_date = forms.DateField(
    #     help_text='Required. Format: mm/dd/yyyy', 
    #     required=False,
    #     label = "Date Of Birth",
    #     widget=forms.DateInput(
    #         attrs={'type': 'date', 'class': 'form-control'}
    #     )
    # )
    phone = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'(xxx)xxx-xxxx'}), required=False)
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder':'Enter valid email'}))
    # image = forms.ImageField(upload_to ="profile_image", blank=True,)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
        
    def clean_email(self):
        """
        Returns the email if entered email is unique otherwise gives duplicate_email error.
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('duplicate_email')
        return email
    