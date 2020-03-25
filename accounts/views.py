from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from accounts.models import Profile, Survey
from boards.models import Board, Post, Topic, MFile
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms.models import inlineformset_factory, formset_factory
from .forms import SignUpForm, UserProfileForm, ProfileForm
from .models import Profile
from django.forms import *
from django.http import JsonResponse
from json import dumps
import json


def login_user(request, *args, **kwargs):
    # if request.method == 'POST':
    #     if not request.POST.get('remember_me', None):
    #         print("un_checked")
    #         # 60 second
    #         request.session.set_expiry(60 * 5)
    return auth_views.login(request, *args, **kwargs)    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not request.POST.get('check_policy', None):
            
            # raise ValidationError("Sorry, that login was invalid. Please try again.")
            # raise PermissionDenied
            
            return render(request, 'signup.html', {'form': form, 'check_policy':'required'})
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # user.profile.fullname = form.cleaned_data.get('fullname')
            # user.profile.nric = form.cleaned_data.get('nric')
            # user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.phone = form.cleaned_data.get('phone')
            # if(request.FILES['avatar']):
            #     user.profile.avatar = request.FILES['avatar']
            user.is_active = False
            
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = "html" #This is the crucial part.
            email.send()
            # Sending activation link in terminal
            # user.email_user(mail_subject, message)
            # return HttpResponse('Please confirm your email address to complete the registration.')
            return render(request, 'acc_active_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('data_survey')
    else:
        return HttpResponse('Activation link is invalid!')
        
        
# @method_decorator(login_required, name='dispatch')
# class UserUpdateView(UpdateView):
    
#     model = User
#     fields = ('username', 'email',)
#     template_name = 'my_account.html'
#     success_url = reverse_lazy('my_account_done')

#     def get_object(self):
#         return self.request.user

@login_required
def data_survey(request):
    if request.method == 'POST':
        error_occured = False
        try:
            # on python 3
            temp = str(request.body, 'utf-8')
            json_data = json.loads(temp)
            
            survey = Survey.objects.create(user=request.user, 
                question = temp
            )
            survey.save()

        except Exception as e:
            error_occured = True
        if error_occured != True:
            data = json.dumps({'url':'/settings/account/survey'})
            return HttpResponse(data)
        else:
            return HttpResponseNotFound('error')
        
    return render(request, 'account_data_survey.html')


@login_required
def data_survey_update(request):
    if request.method == 'POST':
        error_occured = False
        try:
            # on python 3
            temp = str(request.body, 'utf-8')
            json_data = json.loads(temp)
            Survey.objects.filter(user=request.user).update(question=temp)
        except Exception as e:
            error_occured = True
        if error_occured != True:
            data = json.dumps({'url': '/survey/update'})
            return HttpResponse(data)
        else:
            return HttpResponseNotFound('error')
    else:
        try:
            sur = Survey.objects.get(user=request.user)
            survey_json = json.loads(sur.question)

        except:
            return HttpResponse('Survey matching query does not exist.')
        return render(request, 'data_survey_update.html', {'sur':survey_json})


def home(request):
    return render(request, 'home.html')

@login_required
def started(request):
    return render(request, 'get_started.html')


@login_required
def edit_user(request):
    # print(request.user)
    success = 0
    user = request.user
    user_form = UserProfileForm(instance=user)
 
    ProfileInlineFormset = inlineformset_factory(User, Profile, form=ProfileForm, can_delete = False)
    formset = ProfileInlineFormset(instance=user)
    data = Topic.objects.filter(starter=request.user).order_by('-id')[:8]
    files = MFile.objects.all()

 
    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
 
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)                
                # print(formset)

                if formset.is_valid():

                    created_user.save()
                    formset.save()

                    success = 1
                    return render(request, "account_update.html", {
                        "user_form": user_form,
                        "profile_form": formset,
                        "success": success,
                        "data":data,
                        "files":files,
                    })
            success = 2

        return render(request, "account_update.html", {
            "user_form": user_form,
            "profile_form": formset,
            "success":success,
            "data": data,
            "files": files,
        })
    else:
        raise PermissionDenied


def contactus(request):
    return render(request, 'contactus.html')


def forum(request):
    return render(request, 'forum.html')
