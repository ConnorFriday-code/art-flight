from django.shortcuts import render

# Define the profile view
def profile_view(request):
    return render(request, 'profile/profile.html')