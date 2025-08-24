from django.shortcuts import render


def index(request):

    """ A view return the index page """

    return render(request, 'home/index.html')
