from django.shortcuts import render
from .models import Artist

# Create your views here.

def all_artists(request):

    """ A view to return all artists, including sorting and searching """

    artists = Artist.objects.all()

    context = {
        'artists': artists,
    }

    return render(request, 'artists/artists.html', context)