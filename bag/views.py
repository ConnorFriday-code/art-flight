from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user_profile.models import Artist

# Create your views here.

def bag(request):
    """A view to return the bag page"""
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0

    price = {}

    for artist_id, data in bag.items():
        artist = get_object_or_404(Artist, id=artist_id)
        price = artist.price

        for commission in data['commissions']:
            total += commission['price']
            bag_items.append({
                'artist_name': data['artist_name'],
                'commission_option': commission['commission_option'],
                'details': commission['details'],
                'price': commission['price'],
            })

    context = {
        'bag_items': bag_items,
        'price': price,
        'total': total,
    }

    return render(request, 'bag/bag.html', context)

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

def update_commission(request):

    """Update a specific commission in the bag"""
    if request.method == "POST":
        bag = request.session.get('bag', {})
        index = int(request.POST.get('index'))
        artist_id = str(request.POST.get('artist_id'))
        option = request.POST.get('commission_option')
        details = request.POST.get('details')
        price = float(request.POST.get('price'))

        if artist_id in bag and 0 <= index < len(bag[artist_id]['commissions']):
            bag[artist_id]['commissions'][index] = {
                'commission_option': option,
                'price': price,
                'details': details,
            }

            request.session['bag'] = bag
            messages.success(request, "Commission updated successfully!")
        else:
            messages.error(request, "Invalid commission data.")

    return redirect('bag')