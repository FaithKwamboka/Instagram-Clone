from django.shortcuts import render,redirect,get_object_or_404
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        current_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        current_user = None
    if current_user is not None and account_activation_token.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()
        login(request, current_user)
        return HttpResponse('Thank you for your email confirmation. <a href="https://kwashgram.herokuapp.com"> Login </a> Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
    
    
@login_required(login_url='/accounts/login/')
def home(request):
    images = Image.get_images()
    comments = Comment.get_comment()
    profile = Profile.get_profile()

    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.save()
        return redirect('home')

    else:
        form = CommentForm()

    return render(request,"index.html",{"images":images, "comments":comments,"form": form,"profile":profile})


@login_required(login_url='/accounts/login/')
def profile(request,profile_id):

    try:
     profile = Profile.objects.get(pk=profile_id)

    except Profile.DoesNotExist:
      profile = None
      
    images = Image.objects.filter(profile_id=profile).all()

    return render(request,"profile.html",{"profile":profile,"images":images})


@login_required(login_url='/accounts/login/')
def search_results(request):
    current_user = request.user
    profile = Profile.get_profile()
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_name = Profile.find_profile(search_term)
        message = search_term

        return render(request,'search.html',{"message":message,
                                             "profiles":profile,
                                             "user":current_user,
                                             "username":searched_name})
    else:
        message = "You haven't searched for any user"
        return render(request,'search.html',{"message":message})


@login_required(login_url='/accounts/login/')
def get_image_by_id(request,image_id):

    image = Image.objects.get(id = image_id)
    comment = Image.objects.filter(id = image_id).all()

    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.posted_by = current_user
            image.save()
        return redirect('home')

    else:
        form = CommentForm()

    return render(request,"pic.html", {"image":image,"comment":comment,"form": form})

@login_required(login_url='/accounts/login/')
def add_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('home')

    else:
        form = NewProfileForm()
    return render(request, 'new_profile.html', {"form": form})

@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('home')

    else:
        form = NewProfileForm()
    return render(request, 'profile_update.html', {"form": form})


@login_required(login_url='/accounts/login/')
def update_image(request):
    current_user = request.user
    profiles = Profile.get_profile()
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form = UploadForm(request.POST, request.FILES)
                if form.is_valid():
                    upload = form.save(commit=False)
                    upload.posted_by = current_user
                    upload.profile = profile
                    upload.save()
                    return redirect('home')
            else:
                form = UploadForm()
            return render(request, 'upload.html', {"user": current_user, "form": form})


@login_required(login_url='/accounts/login/')
def add_comment(request, pk):
    image = get_object_or_404(Image, pk=pk)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.poster = current_user
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
        return render(request, 'comment.html', {"user": current_user, "comment_form": form})

@login_required(login_url='/accounts/login/')
def like(request,operation,pk):
    image = get_object_or_404(Image,pk=pk)
    
    if operation == 'like':
        image.likes += 1
        image.save()
    elif operation =='unlike':
        image.likes -= 1
        image.save()
    return redirect('home')

@login_required(login_url='/accounts/login/')
def all(request, pk):
    profile = Profile.objects.get(pk=pk)
    images = Image.objects.all().filter(posted_by_id=pk)
    content = {
        "profile": profile,
        'images': images,
    }
    return render(request, 'all.html', content)

@login_required(login_url='/accounts/login/')
def follow(request,operation,id):
    current_user=User.objects.get(id=id)
    if operation=='follow':
        Follow.follow(request.user,current_user)
        return redirect('home')
    elif operation=='unfollow':
        Follow.unfollow(request.user,current_user)
        return redirect('home')
