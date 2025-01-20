from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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
    
def modify_bag(request, id):
    # Retrieve the artist object based on the provided ID
    artist = get_object_or_404(Artist, id=id)

    # Print the artist object to debug and confirm it has an ID
    print(f"Artist object: {artist}")  # This will print the artist object in your console (or logs)

    # If the artist exists, retrieve their price (or other related data)
    price = artist.price

    # Fetch bag items if needed (make sure 'bag_items' exists and is correctly populated)
    bag_items = ...  # Retrieve the bag items from the session or database

    # Pass the artist and other context variables to the template
    context = {
        'artist': artist,
        'price': price,
        'bag_items': bag_items,  # Ensure bag items exist if you're using them
    }

    return render(request, 'bag/bag.html', context)

@csrf_exempt
def update_commission(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        artist = get_object_or_404(Artist, id=id)

        # Update the artist's commission details
        artist.details = data.get("details", artist.details)
        artist.price = data.get("option", artist.price)
        artist.save()

        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)