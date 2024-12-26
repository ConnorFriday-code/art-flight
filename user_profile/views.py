from django.shortcuts import render

# Define the profile view
@login_required
def profile_view(request):
    artist, created = Artist.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        artist.description = request.POST.get('description', artist.description)
        artist.dos = request.POST.get('dos', artist.dos)
        artist.donts = request.POST.get('donts', artist.donts)
        artist.slots = request.POST.get('slots', artist.slots)
        artist.price_options = request.POST.get('price_options', artist.price_options)
        if 'image' in request.FILES:
            artist.image = request.FILES['image']
        artist.save()
        return redirect('profile_view')

    return render(request, 'profile/profile.html', {'artist': artist})