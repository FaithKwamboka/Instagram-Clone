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

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            current_user = form.save(commit=False)
            current_user.is_active = False
            current_user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Kwash Gram account.'
            message = render_to_string('acc_active_email.html', {
                'user': current_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(current_user.pk)),
                'token':account_activation_token.make_token(current_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

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
    
    
@login_required(login_url='/login_backend/')
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

    profile = Profile.objects.get(pk = profile_id)
    images = Image.objects.filter(profile_id=profile).all()

    return render(request,"user_profile.html",{"profile":profile,"images":images})


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

