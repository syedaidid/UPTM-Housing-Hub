from django.shortcuts import render, redirect
from .models import HousingPost
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CreateNewPostForm 
from django.contrib import messages

# Create your views here.

def home(request):
    # Retrieve all housing posts from the database
    posts = HousingPost.objects.all()
    users = User.objects.all()

    for post in posts:
        post.furnished = post.furnished.split(',') if post.furnished else []
        post.facilities = post.facilities.split(',') if post.facilities else []

    context = {
        'posts': posts,  # Pass the posts queryset to the template
        'users': users,

    }
    return render(request, "post/post.html", context)

# def post_detail(request, post_id):
#     return render(request, 'post_detail.html', {'post': post, 'furnished_items': furnished_items})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreateNewPostForm(request.POST)

        if form.is_valid():
            # Create a post instance but don't save it to the database yet
            post = form.save(commit=False)
            # Set the user_id field to the ID of the current user
            post.user_id = request.user.id
            # Save the post to the database
            post.save()
            messages.success(request, 'Your post has been created successfully.')
            return redirect('post-home')
        
            # post = form.save(commit=False)
            # post.author = request.user
            # post.save()
            # messages.success(request, f'Your account has been updated')
            # return redirect('profile')


    else:
        form = CreateNewPostForm()

    context = {
        'form': form,
    }

    return render(request, 'post/create.html', context)