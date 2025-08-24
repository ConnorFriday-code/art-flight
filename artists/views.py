import json
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from user_profile.models import Artist

# Create your views here.


def artist(request):
    # Grab all artists
    artists = Artist.objects.all()

    context = {'artists': artists}

    return render(request, 'artists/artists.html', context)


def all_artists(request):

    """ A view to return all artists, including sorting and searching """

    sort_by = request.GET.get('sort', None)
    tag_filter = request.GET.get('tag', None)
    search_query = request.GET.get('q', None)

    artists = Artist.objects.all()

    with open('artists/fixtures/tags.json', 'r') as f:
        tags = json.load(f)

    if tag_filter:
        normalized_tag = tag_filter.strip().lower().replace(" ", "")

        tag_names = [
            tag['fields']['name']
            .strip()
            .lower()
            .replace(" ", "")
            for tag in tags
        ]

        friendly_names = [
            tag['fields']['friendly_name']
            .strip()
            .lower()
            .replace(" ", "")
            for tag in tags
        ]

        if normalized_tag in tag_names or normalized_tag in friendly_names:
            artists = artists.filter(
                Q(tag__iexact=tag_filter)
                | Q(tag__icontains=tag_filter)
            )

    if search_query:
        artists = artists.filter(
            Q(artist_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(dos__icontains=search_query)
        )

    if sort_by == 'price_low':
        artists = artists.order_by('price')

    elif sort_by == 'price_high':
        artists = artists.order_by('-price')

    context = {
        'artists': artists,
        'tag': tag_filter,
        'sort': sort_by,
        'search_query': search_query,
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
