import os
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CreateService
from .models import Artist
from django.shortcuts import render
from django.conf import settings

# Define the profile view
@login_required
def profile_view(request):

    return render(request, 'profile/profile.html')

@login_required
def create(request):
    if request.method == "POST":
        form = CreateService(request.POST, request.FILES)
        if form.is_valid():
            artist_service = form.save(commit=False)
            artist_service.user = request.user
            artist_service.save()
            return redirect('profile')  # Ensure redirect after successful save
    else:
        form = CreateService()

    # Render the form for both GET requests and invalid POST submissions
    return render(request, 'profile/create.html', {'form': form})