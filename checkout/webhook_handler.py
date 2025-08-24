from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order
from user_profile.models import UserProfile
import stripe


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_order_emails(self, order):
        """Send confirmation email to user and notification to artists"""
        # Email to user
        subject_user = f"Order Confirmation - {order.order_number}"
        body_user = render_to_string(
            "emails/order_confirmation.txt",
            {
                "order": order,
                "contact_email": settings.DEFAULT_FROM_EMAIL,
            },
        )
        send_mail(
            subject_user,
            body_user,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=False,
        )

        # Email to each artist
        for line_item in order.lineitems.all():
            artist_email = line_item.artist.email
            subject_artist = (
                f"New Commission Order from {order.full_name}"
            )
            body_artist = render_to_string(
                "emails/artist_notification.txt",
                {
                    "order": order,
                    "line_item": line_item,
                    "contact_email": settings.DEFAULT_FROM_EMAIL,
                },
            )
            send_mail(
                subject_artist,
                body_artist,
                settings.DEFAULT_FROM_EMAIL,
                [artist_email],
                fail_silently=False,
            )

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        return HttpResponse(
            content=(
                f"Unhandled webhook received: {event['type']}"
            ),
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        intent = event.data.object
        pid = intent.id

        try:
            order = Order.objects.get(stripe_pid=pid)
            self._send_order_emails(order)
            return HttpResponse(
                content=(
                    f"Webhook received: {event['type']} | "
                    "SUCCESS: Verified order in DB"
                ),
                status=200,
            )
        except Order.DoesNotExist:
            return HttpResponse(
                content=(
                    f"Webhook received: {event['type']} | "
                    "ERROR: Order not found in DB"
                ),
                status=404,
            )

    def handle_payment_intent_failed(self, event):
        """Handle the payment_intent.failed webhook from Stripe"""
        return HttpResponse(
            content=f"Webhook received: {event['type']}",
            status=200,
        )
