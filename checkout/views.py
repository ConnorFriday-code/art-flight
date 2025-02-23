from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Order, OrderLineItem
from .forms import OrderForm
from bag.contexts import bag_contents
from user_profile.models import Artist
import stripe


def checkout(request):
    """ Handles checkout process and order creation """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)

            order.save()
            for artist_id, data in bag.items():
                try:
                    artist = get_object_or_404(Artist, id=artist_id)
                    
                    for commission in data['commissions']:
                        print(f"Price being saved: {commission['price']} (type: {type(commission['price'])})")
                        order_line_item = OrderLineItem(
                            order=order,
                            artist=artist,
                            commission_option=commission['commission_option'],
                            details=commission['details'],
                            price=commission['price'],
                        )
                        order_line_item.save()

                except Artist.DoesNotExist:
                    messages.error(request, (
                        "One of the artists in your bag was not found. "
                        "Please contact support for assistance."
                    ))
                    order.delete()
                    return redirect(reverse('bag'))

            # Save order info for user profiles (optional)
            request.session['save_info'] = 'save-info' in request.POST

            # Clear the session bag after checkout
            request.session['bag'] = {}

            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please check your details.')

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment.")
            return redirect(reverse('artists'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. Did you set it in your environment variables?')

        order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request,order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed!\
                     Your order number is {order_number}.A confirmation\
                        email will be sent to {order.email}.')
    
    if 'bag' in request.session:
        del request.session['bag']
    
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)