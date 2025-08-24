from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from checkout.models import Order
from .forms import CreateService
from .models import Artist


# Render profile
@login_required
def profile_view(request):
    return render(request, "profile/profile.html")


# Create new artist advert/post
@login_required
def create(request):
    if request.method == "POST":
        form = CreateService(request.POST, request.FILES)
        if form.is_valid():
            artist_service = form.save(commit=False)
            artist_service.user = request.user
            artist_service.save()
            return redirect("profile")
    else:
        form = CreateService()

    return render(request, "profile/create.html", {"form": form})


# Edit artist post/advert
def edit(request, pk):
    artist = get_object_or_404(Artist, pk=pk, user=request.user)

    if request.method == "POST":
        form = CreateService(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = CreateService(instance=artist)

    return render(
        request,
        "profile/edit.html",
        {"form": form, "artist": artist},
    )


# Delete artist post or advert
def delete_artist(request, pk):
    artist = get_object_or_404(Artist, pk=pk, user=request.user)

    if request.method == "POST":
        artist.delete()
        return redirect("profile")

    return render(request, "profile/profile.html")


# Display all orders
@login_required
def order_list(request):
    """Display all orders for the logged-in user"""
    orders = (
        Order.objects.filter(user_profile__user=request.user)
        .order_by("-date")
    )

    return render(request, "profile/order_list.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
    """Display the details of a specific order"""
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user_profile__user=request.user,
    )

    return render(request, "checkout/checkout_success.html", {"order": order})
