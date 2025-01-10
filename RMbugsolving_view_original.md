The original view for displaying artists:

~~~

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from user_profile.models import Artist

# Create your views here.

def artist(request):
    #Grab all artists
    artists = Artist.objects.all()

    context = {'artists': artists}
    
    return render(request, 'artists/artists.html', context)

def all_artists(request):

    """ A view to return all artists, including sorting and searching """

    sort_by = request.GET.get('sort',None)
    tag_filter = request.GET.get('tag',None)
    search_query = request.GET.get('q',None)

    #Grab all artists
    artists = Artist.objects.all()

    #Nav bar tag filter
    if tag_filter:
        artists = artists.filter(tag=tag_filter)
    
    #Nav search bar filter
    if search_query:
        artists =artists.filter(
            Q(artist_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(dos__icontains=search_query)
        )

    #Sort artists by price, lowest first
    if sort_by=='price_low':
        artists = artists.order_by('price') 
    #Sort artists by price, highest first
    elif sort_by=='price_high':
        artists = artists.order_by('-price')

    context = {
        'artists': artists,
        'tag':tag_filter,
        'sort': sort_by,
        'search_query':search_query,
    }

    return render(request, 'artists/artists.html', context)

    ~~~