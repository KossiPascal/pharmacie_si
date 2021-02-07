from med.templatetags.functions_extras import LoggedInSuccessMessage, UserIsConnect, InactiveAccountMessage, IncorectLoginInfosMessage, SuccessUpdateMessage, SuccessSaveMessage, RequireAuthenticateMessage, LogoutSuccessMessage
from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileInfoForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfileInfo

from django.contrib import messages

def user_register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        profile_pic = request.POST.get('profile_pic')
        user = authenticate(username=username, password=password)
        if password == password_confirm:
            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                if profile_pic != "":
                    profile.profile_pic = request.FILES['profile_pic']
                    profile.profile_pic_thumb = request.FILES['profile_pic']

                try:
                    profile.save()
                    login(request, user)
                    datas = UserProfileInfo.objects.filter(user_id=str(user.id))
                    for data in datas:
                        request.session['small_user_profile_img_url'] = str(data.profile_pic_thumb)
                        request.session['large_user_profile_img_url'] = str(data.profile_pic)
                    registered = True
                    messages.success(request, SuccessSaveMessage(request))
                    return HttpResponseRedirect(reverse('profile'))
                except:
                    pass
            else:
                print(user_form.errors, profile_form.errors)
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
   
    return render(request, 'auths/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'go_to_previous_page': UserIsConnect(request), 'text_transform':True})
 
def user_login(request):
    error = ""    

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nxt = request.POST.get('next')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                datas = UserProfileInfo.objects.filter(user_id=request.user.id)

                for data in datas:
                    request.session['small_user_profile_img_url'] = str(data.profile_pic_thumb)
                    request.session['large_user_profile_img_url'] = str(data.profile_pic)
                
                messages.info(request, LoggedInSuccessMessage(request))
                if nxt:
                    return redirect(nxt)
                else:
                    return HttpResponseRedirect(reverse('home'))
            else:
                error = InactiveAccountMessage(request)
        else:
            error = IncorectLoginInfosMessage(request)
      
    return render(request, 'auths/login.html', {'error': error, 'go_to_previous_page': UserIsConnect(request), 'text_transform': True})

@login_required
def user_profile(request):
    Image_is_not_save = False
    query_user = User.objects.get(pk=request.user.id)
    Image_profile_form = UserProfileInfoForm(data=request.POST)

    if UserProfileInfo.objects.filter(user_id=request.user.id):
        query_profile = UserProfileInfo.objects.get(user_id=request.user.id)
        profile_form = UserProfileInfoForm(instance=query_profile)
    else:
        profile_form = UserProfileInfoForm()

    user_form = ProfileForm(instance=query_user)
    
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        pic = request.POST.get('profile_pic')

        if UserProfileInfo.objects.filter(user_id=request.user.id):
            profile = UserProfileInfo.objects.get(user_id=request.user.id)
            if pic != "":
                profile.delete()
        else:
            profile = profile_form.save(commit=False)
            profile.user = user

        if pic != "":
            profile.profile_pic = request.FILES['profile_pic']
            profile.profile_pic_thumb = request.FILES['profile_pic']

        profile.biography = request.POST.get('biography')

        try:
            profile.save()
            messages.success(request, SuccessUpdateMessage(request))
            return HttpResponseRedirect(reverse('profile'))
        except:
            Image_is_not_save = True

    datas = UserProfileInfo.objects.filter(user_id=request.user.id)

    for data in datas:
        request.session['small_user_profile_img_url'] = str(data.profile_pic_thumb)
        request.session['large_user_profile_img_url'] = str(data.profile_pic)
    return render(request, 'auths/profiles.html', {"user_form": user_form, 'profile_form': profile_form, 'Image_profile_form': Image_profile_form, 'Image_is_not_save': Image_is_not_save})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, LogoutSuccessMessage(request))
    else:
        messages.info(request, RequireAuthenticateMessage(request))
    
    return HttpResponseRedirect(reverse('login'))

def user_params(request):
    return render(request, 'auths/userparams.html', {})
