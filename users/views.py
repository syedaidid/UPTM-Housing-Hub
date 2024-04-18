from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from post.models import HousingPost
from .models import Profile

from .signals import edit_profile

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {'form': form})

from django.core.cache import cache

# ... (other imports)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            # Clear all cache
            cache.clear()

            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Retrieve posts made by the current user
    user_posts = HousingPost.objects.filter(user=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': user_posts  # Add user's posts to the context
    }

    return render(request, 'users/profile.html', context)