from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

def checkout(request):
    bag = request.session.get('bag', {})

    if not bag:
        message.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('artists'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51QsyYGByzIN8bZpUlt6XEY1oWFqYfVRTgV1IaMDYibrKVhpNZQ3xvlTbYlserTU322C1zgMRFdRfyzIBSwRYoxSf00WOIkeEWX',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
