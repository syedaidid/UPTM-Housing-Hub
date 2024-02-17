from django.shortcuts import render, redirect
from .models import HousingPost, Image
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CreateNewPostForm, ImageForm
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def create_post(request):
    if request.method == "POST":
        form = CreateNewPostForm(request.POST)
        imageform = ImageForm(request.POST, request.FILES)
        if form.is_valid() and imageform.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            for image in request.FILES.getlist("image"):
                Image.objects.create(housing_post=post, image=image)
            return render(request, "post/post.html")
    else:
        form = CreateNewPostForm()
        imageform = ImageForm()
    context = {
        'form': form,
        'imageform': imageform,
    }
    return render(request, "post/create.html", context)

# Create your views here.

# def home(request):
#     # Retrieve all housing posts from the database
#     posts = HousingPost.objects.all()

#     for post in posts:
#         post.furnished = post.furnished.split(',') if post.furnished else []
#         post.facilities = post.facilities.split(',') if post.facilities else []

#     context = {
#         'posts': posts,  # Pass the posts queryset to the template
#     }
#     return render(request, "post/post.html", context)

class PostListView(View):
    def get(self, request):
        posts = HousingPost.objects.order_by('-date_posted').all()
        for post in posts:
            post.furnished = post.furnished.split(',') if post.furnished else []
            post.facilities = post.facilities.split(',') if post.facilities else []
        return render(request, "post/post.html", {'posts': posts})

class PostDetailView(View):
    def get(self, request, pk):
        # Retrieve the HousingPost object with the given primary key (pk)
        post = HousingPost.objects.get(pk=pk)
        # Split the furnished and facilities fields into lists
        post.furnished = post.furnished.split(',') if post.furnished else []
        post.facilities = post.facilities.split(',') if post.facilities else []
        # Pass the modified post object to the template
        context = {'object': post}
        return render(request, 'post/detail.html', context) 

        
class PostCreateView(LoginRequiredMixin, CreateView):
    model = HousingPost
    fields = ['title', 'description', 'gender', 'number_of_people', 'deposit', 'monthly_payment', 'furnished', 'facilities']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
     

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = HousingPost
    fields = ['title', 'description', 'gender', 'number_of_people', 'deposit', 'monthly_payment', 'furnished', 'facilities']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = HousingPost
    success_url = '/posts'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


# @login_required
# def create_post(request):
#     if request.method == 'POST':
#         form = CreateNewPostForm(request.POST)

#         if form.is_valid():
#             # Create a post instance but don't save it to the database yet
#             post = form.save(commit=False)
#             # Set the user_id field to the ID of the current user
#             post.user_id = request.user.id
#             # Save the post to the database
#             post.save()
#             messages.success(request, 'Your post has been created successfully.')
#             return redirect('post-home')
        
#             # post = form.save(commit=False)
#             # post.author = request.user
#             # post.save()
#             # messages.success(request, f'Your account has been updated')
#             # return redirect('profile')


#     else:
#         form = CreateNewPostForm()

#     context = {
#         'form': form,
#     }

#     return render(request, 'post/create.html', context)