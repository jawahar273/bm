from django.conf import settings
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def send_mail(self, template_prefix, email, context):
        context[
            "activate_url"
        ] = settings.CLIENT_REDIRECT_DOMAIN + "confirm-email/{}/".format(context["key"])
        msg = self.render_mail(template_prefix, email, context)
        msg.send()

    # def get_email_confirmation_url(self, request, emailconfirmation):

    #     url = reverse(
    #         "account_confirm_email",
    #         args=[emailconfirmation.key])

    #     return settings.CLIENT_REDIRECT_DOMAIN + url


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
