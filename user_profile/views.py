from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CreateService

# Define the profile view
@login_required
def profile_view(request):

    return render(request, 'profile/profile.html')

def create(request):

    if request.method == "POST":
        form = CreateService(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile or another page after submission
    else:
        form = CreateService()

    return render(request, 'profile/create.html', {'form': form})