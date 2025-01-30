import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateService
from .models import Artist
from django.conf import settings

# Render profile
@login_required
def profile_view(request):

    return render(request, 'profile/profile.html')

#Create new artist advert/post
@login_required
def create(request):
    if request.method == "POST":
        form = CreateService(request.POST, request.FILES)
        if form.is_valid():
            artist_service = form.save(commit=False)
            artist_service.user = request.user
            artist_service.save()
            return redirect('profile')
    else:
        form = CreateService()

    return render(request, 'profile/create.html', {'form': form})


# Edit artist post/advert
def edit(request, pk):
    artist = get_object_or_404(Artist, pk=pk, user=request.user)

    if request.method == "POST":
        form = CreateService(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CreateService(instance=artist)

    return render(request, 'profile/edit.html', {'form': form, 'artist': artist})

# Delete artist post or advert
def delete_artist(request, pk):
    artist = get_object_or_404(Artist, pk=pk, user=request.user)

    if request.method == "POST":
        artist.delete()
        return redirect('profile')

    return render(request, 'profile/profile.html')