from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from user_profile.models import Artist
from django.http import JsonResponse
import uuid

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
                'bag_id': commission['bag_id'],
                'artist_id': artist.id,
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
    bag_id = str(uuid.uuid4()) 

    artist = get_object_or_404(Artist, id=artist_id)

    item = {
        'bag_id': bag_id,
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


def edit_bag(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    if request.method == 'POST':
        # Extract submitted form data
        bag_id = request.POST.get('bag_id')  # Get bag_id from the form
        new_option = request.POST.get('commission_option')  # Get updated option
        new_details = request.POST.get('edit_details')  # Get updated details

        bag = request.session.get('bag', {})

        # Find and update the specific item in the bag
        if str(artist_id) in bag:  # Ensure artist exists in the session bag
            for commission in bag[str(artist_id)]['commissions']:
                if commission['bag_id'] == bag_id:  # Match the correct commission
                    # Update the item
                    commission['commission_option'] = new_option
                    commission['details'] = new_details
                    commission['price'] = artist.price[new_option]  # Update price
                    break

        # Save the updated bag to the session
        request.session['bag'] = bag
        request.session.modified = True  # Mark session as modified

        messages.success(request, f"Updated your commission for {artist.artist_name}.")
        return redirect('bag')  # Redirect back to the bag page

    # If GET request, render the edit form
    bag_id = request.GET.get('bag_id', '')
    details = request.GET.get('details', '')
    commission_option = request.GET.get('commission_option', '')

    context = {
        'artist': artist,
        'bag_id': bag_id,
        'details': details,
        'commission_option': commission_option,
        'price': artist.price,
    }
    return render(request, 'bag/edit_bag.html', context)

def remove_commission(request, bag_id):
    """Remove a commission from the bag"""
    bag = request.session.get('bag', {})
    
    # Iterate through all items and remove the one with the matching bag_id
    for artist_id in list(bag.keys()):
        bag[artist_id]['commissions'] = [
            commission for commission in bag[artist_id]['commissions']
            if commission['bag_id'] != bag_id
        ]

        # Remove artist from bag if no commissions are left
        if not bag[artist_id]['commissions']:
            bag.pop(artist_id)
    
    # Save the updated bag in the session
    request.session['bag'] = bag
    request.session.modified = True

    return JsonResponse({'success': True, 'bag_id': bag_id})