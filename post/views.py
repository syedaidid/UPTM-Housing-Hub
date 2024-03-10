from django.shortcuts import render, redirect, get_object_or_404
from .models import HousingPost, Image
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CreateNewPostForm, ImageForm, PostUpdateForm
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import HousingPostFilter

class UserDetailView(View):
    def get(self, request, pk):
        # Retrieve the user object with the given primary key (pk)
        user = User.objects.get(pk=pk)
        
        # Pass the user object to the template
        context = {
            'user': user,
        }
        return render(request, 'users/detail.html', context)

@login_required
def create_post(request):
    form = CreateNewPostForm()
    
    if request.method == "POST":
        form = CreateNewPostForm(request.POST)
        images = request.FILES.getlist('image')

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            for i in images:
                Image.objects.create(housing_post=post, image=i)
            return redirect('post-home')
    
    context = {'form': form}
    return render(request, "post/create.html", context)

def update_post(request, pk):
    post = get_object_or_404(HousingPost, pk=pk)
    if request.method == 'POST':
        form = CreateNewPostForm(request.POST, instance=post)
        images = request.FILES.getlist('image')
        if form.is_valid():
            form.save()
            for i in images:
                Image.objects.create(housing_post=post, image=i)
            return redirect('post-detail', pk=pk)
    else:
        form = CreateNewPostForm(instance=post)
    
    context = {'form': form, 'post': post}
    return render(request, "post/update.html", context)

def delete_images(request):
    if request.method == 'POST':
        selected_image_ids = request.POST.getlist('selected_images')
        for image_id in selected_image_ids:
            image = Image.objects.get(id=image_id)
            image.delete()
    return redirect('post-home')  # Redirect to the desired view after deletion

class PostListView(View):
    def get(self, request):
        posts = HousingPost.objects.order_by('-date_posted').all()
        myFilter = HousingPostFilter(request.GET, queryset=posts)
        posts = myFilter.qs

        # Process each post to split furnished and facilities fields into lists
        for post in posts:
            post.furnished = post.furnished.split(',') if post.furnished else []
            post.facilities = post.facilities.split(',') if post.facilities else []
            post.accessibilities = post.accessibilities.split(',') if post.accessibilities else []

        context = {
            'posts': posts,
            'myFilter': myFilter
        }
        return render(request, "post/post.html", context)

import folium
from geocoder import osm
from django.urls import reverse

class PostDetailView(View):
    def get(self, request, pk):
        # Retrieve the HousingPost object with the given primary key (pk)
        post = HousingPost.objects.get(pk=pk)

        # Construct the URL to the detail page of the post
        post_detail_url = reverse('post-detail', kwargs={'pk': post.pk})
        popup_html = f'<a href="{post_detail_url}" target="_blank">{post.title}</a>'

        # Split the furnished and facilities fields into lists
        post.furnished = post.furnished.split(',') if post.furnished else []
        post.facilities = post.facilities.split(',') if post.facilities else []
        post.accessibilities = post.accessibilities.split(',') if post.accessibilities else []

        # Use geocoder to get the coordinates of a location (in this case, UK)
        location = osm(post.address)
        lat = location.lat
        lng = location.lng

        # Check if both latitude and longitude are valid
        if lat is not None and lng is not None:
            # Create a Folium map centered at coordinates [lat, lng] with zoom level 20
            m = folium.Map(location=[lat, lng], zoom_start=20)

            # Add a marker to the map
            folium.Marker([lat, lng], tooltip='', popup=popup_html).add_to(m)

            # Pass the map to the template
            context = {
                'object': post,
                'm': m._repr_html_(),  # Convert Folium map to HTML
            }
            return render(request, 'post/detail.html', context)
        else:
            # If location cannot be found, return a response without rendering the map
            return render(request, 'post/detail.html', {'object': post})

class PostListMapView(View):
    def get(self, request):
        posts = HousingPost.objects.all()
        m = folium.Map(location=[3.127879824059893, 101.73731112157995], zoom_start=15)

        # Dictionary to store the count of posts for each unique address
        address_counts = {}

        for post in posts:
            # Retrieve location coordinates for the address
            location = osm(post.address)

            # Check if both latitude and longitude are valid
            if location.ok:  # Check if location was found successfully
                lat = location.latlng[0]
                lng = location.latlng[1]

                # Get the count of posts for this address
                count = address_counts.get(post.address, 0)

                # Add a small offset to latitude and longitude for each marker
                lat_offset = 0.0002 * count
                lng_offset = 0.0002 * count

                # Construct the URL for the post detail page
                post_url = reverse('post-detail', kwargs={'pk': post.pk})  # Adjust 'post-detail' to the name of your post detail URL

                # Create a link to the post detail page in the popup
                popup_html = f'<a href="{post_url}" target="_blank">{post.title}</a>'

                # Add a marker to the map with the link in the popup
                folium.Marker([lat + lat_offset, lng + lng_offset], tooltip='', popup=popup_html).add_to(m)

                # Update the count of posts for this address
                address_counts[post.address] = count + 1

        context = {
            'object': posts,
            'm': m._repr_html_(),  # Convert Folium map to HTML
        }

        return render(request, 'post/map.html', context)
        
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