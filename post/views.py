from django.contrib.auth import get_user_model
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
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

class UserDetailView(View):
    def get(self, request, pk):
        # Retrieve the user object with the given primary key (pk)
        user = get_object_or_404(User, pk=pk)
        
        # Retrieve housing posts associated with the user
        user_posts = HousingPost.objects.filter(user=user)
        
        # Pass the user and housing posts to the template
        context = {
            'user': user,
            'posts': user_posts,
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
        pk = request.POST.get('post_id')  # Retrieve the post_id from POST data
        selected_image_ids = request.POST.getlist('selected_images')
        for image_id in selected_image_ids:
            image = Image.objects.get(id=image_id)
            image.delete()
    return redirect('post-update', pk=pk)

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
        cache_key = f'post_detail_{pk}'
        cached_html = cache.get(cache_key)

        if cached_html is not None:
            return cached_html

        post = HousingPost.objects.get(pk=pk)
        html = self.render_post_detail(request, post)
        cache.set(cache_key, html, 60 * 60)  # Cache for 1 hour
        return html

    def render_post_detail(self, request, post):
        post_detail_url = reverse('post-detail', kwargs={'pk': post.pk})
        popup_html = f'<a href="{post_detail_url}" target="_blank">{post.title}</a>'

        post.furnished = post.furnished.split(',') if post.furnished else []
        post.facilities = post.facilities.split(',') if post.facilities else []
        post.accessibilities = post.accessibilities.split(',') if post.accessibilities else []

        if post.address:
            location = osm(post.address)
            lat = location.lat
            lng = location.lng

            if lat is not None and lng is not None:
                m = folium.Map(location=[lat, lng], zoom_start=20)
                folium.Marker([lat, lng], tooltip='', popup=popup_html).add_to(m)
                map_html = m._repr_html_()
                context = {
                    'object': post,
                    'm': map_html,
                }
                return render(request, 'post/detail.html', context)

        # If location cannot be found, render without map
        return render(request, 'post/detail.html', {'object': post}) 

class PostListMapView(View):
    def get(self, request):
        cache_key = 'post_list_map'
        cached_html = cache.get(cache_key)

        if cached_html is not None:
            return cached_html

        posts = HousingPost.objects.all()
        map_html = self.generate_map(posts)
        context = {
            'object': posts,
            'm': map_html,
        }
        rendered_html = render(request, 'post/map.html', context)
        cache.set(cache_key, rendered_html, 60 * 60)
        return rendered_html
    
    def generate_map(self, posts):
        m = folium.Map(location=[3.127879824059893, 101.73731112157995], zoom_start=15)
        address_counts = {}

        for post in posts:
            location = osm(post.address)
            if location.ok:
                lat = location.latlng[0]
                lng = location.latlng[1]
                count = address_counts.get(post.address, 0)
                lat_offset = 0.0002 * count
                lng_offset = 0.0002 * count

                post_url = reverse('post-detail', kwargs={'pk': post.pk})
                popup_html = f'<a href="{post_url}" target="_blank">{post.title}</a>'

                folium.Marker([lat + lat_offset, lng + lng_offset], tooltip='', popup=popup_html).add_to(m)
                address_counts[post.address] = count + 1

        return m._repr_html_()
        
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

@cache_page(60*15)
def cached(request):
    user_model = get_user_model()
    all_users = user_model.objects.all()
    return HttpResponse('<html><body><h1>{0} users... cached</h1></body></html>'.
                        format(len(all_users)))
    
def cacheless(request):
    user_model = get_user_model()
    all_users = user_model.objects.all()
    return HttpResponse('<html><body><h1>{0} users... cacheless</h1></body></html>'.
                        format(len(all_users)))