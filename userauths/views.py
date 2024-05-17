from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from userauths.models import Profile
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from core.models import Post,FriendRequest
from django.views.decorators.csrf import csrf_protect
# Create your views here.


@csrf_protect
def registration(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered')
        return redirect('index')

    form = UserRegistrationForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()

        full_name = form.cleaned_data.get('full_name')
        phone = form.cleaned_data.get('phone')
        email = form.cleaned_data.get('email')

        # Authenticate the user
        user = authenticate(email=email, password=form.cleaned_data['password1'])
        login(request, user)

        # Create or update the user's profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        messages.success(request, f'{full_name}, your account was created successfully')
        return redirect('index')

    context = {
        "form": form
    }

    return render(request, 'userauths/signup.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth

def loginview(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are successfully logged in')
            return redirect('index')  # Redirect to the 'index' URL after successful login
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('register')  # Redirect to the 'register' URL if login is unsuccessful
    else:
        return render(request, 'userauths/signup.html')  # Render the 'signup.html' template for GET requests

            
def logout(request):
    auth.logout(request)
    return redirect('register')
    
def logout_view(request):

        logout(request)
        return redirect('admin:index')
@login_required
def my_profile(request):
    profile=request.user.profile
    post=Post.objects.filter(active=True,user=request.user).order_by('-id')
    context={
        'profile':profile,
        'posts':post
    }
    
    return render(request,'userauths/my_profile.html',context)
    
@login_required
def friend_profile(request,username):
    profile=Profile.objects.get(user__username=username)
    if request.user.profile == profile:
        redirect('my_profile')
    post=Post.objects.filter(active=True,user=profile.user).order_by('-id')
    
    bool=False
    bool_friend=False
    sender=request.user
    receiver=profile.user
    
    try:
        friend_request=FriendRequest.objects.get(sender=sender,receiver=receiver)
        if friend_request:
            bool=True
        else:
            bool=False
        
    except:
        bool=False
        
    
    context={
        'profile':profile,
        'posts':post,
        'bool':bool
    }
    
  
    
    return render(request,'userauths/friend_profile.html',context)
    