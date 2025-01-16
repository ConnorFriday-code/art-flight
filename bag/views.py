from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.

def bag(request):

    """ A view return the bag page """

    return render(request, 'bag/bag.html')