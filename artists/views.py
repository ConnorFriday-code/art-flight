import json
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

    #Open the json file and load tags
    with open('artists/fixtures/tags.json', 'r') as f:
        tags = json.load(f)

    #Nav bar tag filter
    if tag_filter:
        # Replace all space with nothing and lower case everything
        normalized_tag = tag_filter.strip().lower().replace(" ", "")

        #Grab tag names and freindly names from json file
        #Then remove all spaces and lowercase everything (future proof future tags)
        tag_names = [
            tag['fields']['name'].strip().lower().replace(" ", "") for tag in tags
        ]
        friendly_names = [
            tag['fields']['friendly_name'].strip().lower().replace(" ", "") for tag in tags
        ]

        #Check if the normalized_tag matches either name or friendly_name
        if normalized_tag in tag_names or normalized_tag in friendly_names:
            #Filter artists where the tag matches case-insensitively
            artists = artists.filter(
                #Checks the artists' tags against the ones in the json file using exact inputs
                Q(tag__iexact=tag_filter)
                #Checks the artists' tags against the ones in the json file without spacing/capitals
                | Q(tag__icontains=tag_filter)  
            )
    
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

def artists_details(request, sku):

    """ A view to return a specified artist """

    artist = get_object_or_404(Artist, sku=sku)
    tag = artist.tag
    price = artist.price

    context = {
        'artist': artist,
        'tag': tag,
        'price': price,
    }

    return render(request, 'artists/artists_details.html', context)