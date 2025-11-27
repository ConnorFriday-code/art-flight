from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order
import stripe


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        # Store the original request for later use
        self.request = request

    def _send_order_emails(self, order):
        """Send the order confirmation email to the customer"""

        # Prepare email content for the customer
        subject_user = f"Order Confirmation - {order.order_number}"
        body_user = render_to_string(
            "emails/order_confirmation.txt",
            {
                "order": order,
                "contact_email": settings.DEFAULT_FROM_EMAIL,
            },
        )

        # Send email to the customer's email address
        send_mail(
            subject_user,
            body_user,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=False,
        )

    def handle_event(self, event):
        """Handle any unexpected webhook events"""
        return HttpResponse(
            content=f"Unhandled webhook received: {event['type']}",
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle successful Stripe payments"""

        # Get the payment intent object from Stripe
        intent = event.data.object
        pid = intent.id

        try:
            # Try to find the matching order in the database
            order = Order.objects.get(stripe_pid=pid)

            # If found, send confirmation email
            self._send_order_emails(order)

            return HttpResponse(
                content=(
                    f"Webhook received: {event['type']} | "
                    "SUCCESS: Verified order in DB"
                ),
                status=200,
            )

        except Order.DoesNotExist:
            # If no order was found for this payment
            return HttpResponse(
                content=(
                    f"Webhook received: {event['type']} | "
                    "ERROR: Order not found in DB"
                ),
                status=404,
            )

    def handle_payment_intent_failed(self, event):
        """Handle failed Stripe payments"""
        return HttpResponse(
            content=f"Webhook received: {event['type']}",
            status=200,
        )
    