from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user_profile.models import Artist

# Create your views here.

def bag(request):

    """ A view return the bag page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, id):
    """Add a commission to the shopping bag"""

    artist_id = request.POST.get('artist_id')
    commission_option = request.POST.get('commission_option')
    commission_details = request.POST.get('commission_details')
    redirect_url = request.POST.get('redirect_url') 

    artist = get_object_or_404(Artist, id=artist_id)

    item = {
        'artist_name': artist.artist_name,
        'commission_option': commission_option,
        'price': artist.price[commission_option],
        'details': commission_details,
    }

    bag = request.session.get('bag', {})

    if artist_id in bag:
        bag[artist_id]['commissions'].append(item)
    else:
        bag[artist_id] = {
            'artist_name': artist.artist_name,
            'commissions': [item],
        }

    request.session['bag'] = bag

    messages.success(request, f"Added a commission for {artist.artist_name} to your bag!")

    return redirect(redirect_url)