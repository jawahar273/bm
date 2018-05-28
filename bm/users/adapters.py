from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def send_mail(self, template_prefix, email, context):
        context["activate_url"] = (
            settings.BM_CLIENT_CROSS_DOMAIN_NAME + "confirm-email/" + context["key"]
        )
        msg = self.render_mail(template_prefix, email, context)
        msg.send()


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
