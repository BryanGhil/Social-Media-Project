from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, PostForm
from .models import Post, User
from django.db.models import F

def home(request):
    posts = Post.objects.all()
    posts = posts.annotate(author_username=F('author__username'))

    context = {
        'posts': posts
    }
    return render(request, 'home.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out ...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered")

            return redirect('home')
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(request, "Post Added Successfully")
                return redirect('home')
        else:
            form = PostForm()
        return render(request, 'create_post.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In To Do That")
        return redirect('home')
    
def delete_post(request, post_id):
    if request.user.is_authenticated: 
        delete_it = Post.objects.get(id=post_id)
        delete_it.delete()
        messages.success(request, "Post Deleted Successfully")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Do That")
        return redirect('home')
    
def likes_post(request, post_id):
    if request.user.is_authenticated: 
        select_post = Post.objects.get(id=post_id)
        select_post.likes += 1
        select_post.save()
        messages.success(request, "You Like This Post")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Do That")
        return redirect('home')