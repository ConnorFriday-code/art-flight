from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Artist
from django.http import JsonResponse

# Create your views here.

def all_artists(request):

    """ A view to return all artists, including sorting and searching """

    sort_by = request.GET.get('sort',None)
    tag_filter = request.GET.get('tag',None)
    search_query = request.GET.get('q',None)

    artists = Artist.objects.all()

    if tag_filter:
        artists = artists.filter(tag__name=tag_filter)
    
    if search_query:
        artists =artists.filter(
            Q(artist_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(dos__icontains=search_query)
        )

    if sort_by=='price_low':
        artists = artists.order_by('price') 
    elif sort_by=='price_high':
        artists = artists.order_by('-price')

    context = {
        'artists': artists,
        'tag':tag_filter,
        'sort': sort_by,
        'search_query':search_query,
    }

    return render(request, 'artists/artists.html', context)

def artists_details(request, sku):

    """ A view to return a specified artist """

    artist = get_object_or_404(Artist, sku=sku)
    tag = artist.tag.name

    context = {
        'artist': artist,
        'tag': tag,
    }

    return render(request, 'artists/artists_details.html', context)