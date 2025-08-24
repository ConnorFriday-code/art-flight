from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from user_profile.models import Artist


def bag_contents(request):

    bag_items = []
    total = Decimal(0)
    product_count = 0

    bag = request.session.get('bag', {})

    for artist_id, data in bag.items():
        artist = get_object_or_404(Artist, id=artist_id)

        for commission in data['commissions']:
            price = Decimal(commission['price'])
            total += price
            bag_items.append({
                'artist_id': artist_id,
                'artist_name': artist.artist_name,
                'commission_option': commission['commission_option'],
                'price': commission['price'],
                'details': commission['details'],
            })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
