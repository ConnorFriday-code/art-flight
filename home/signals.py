from allauth.account.signals import email_added
from allauth.account.models import EmailAddress
from django.dispatch import receiver


@receiver(email_added)
def fix_email_flags_on_add(request, user, emailaddress, **kwargs):
    """
    Prevents an email from being both unverified and primary.
    Ensures only one primary email exists per user.
    """
    EmailAddress.objects.filter(user=user).exclude(id=emailaddress.id).update(primary=False)

    if emailaddress.primary and not emailaddress.verified:
        emailaddress.primary = False
        emailaddress.save()