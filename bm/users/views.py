import urllib.parse

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from allauth.account import views as allauth_views

from .models import User


@csrf_exempt
@api_view(['GET'])
def redirect_password_rest_done(request, uidb64, token):
    return redirect(urllib.parse.urljoin(settings.CLIENT_REDIRECT_DOMAIN,
                    '%s/%s/%s' % (settings.CLIENT_REDIRECT_URL, uidb64, token))
                    )


def display_home_page(request):
    '''
    An index function to show the home.
    '''
    msg = 'Mail Gun has a problem so, no new account are allowed to register'
    messages.warning(request, msg)
    return render(request, 'pages/home.html')


def redirect_after_email_confirm(request):
    '''
    Allow for redirection in server side from email.
    '''
    return render(request, 'account/after_email_validation_confirm.html')


class LoginAfterPasswordChangeView(allauth_views.PasswordChangeView):
    template_name = 'account/password_rest_done.html'

    @property
    def success_url(self):
        return reverse_lazy('change_password_done')


login_after_password_change = LoginAfterPasswordChangeView.as_view()


class UserDetailView(LoginRequiredMixin, DetailView):
    '''
    .. deprecated::
       This class may deprecated after review as it not useful in production
    '''
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    '''
    .. deprecated::
       This class may deprecated after review as it not useful in production
    '''
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    '''
    .. deprecated::
       This class may deprecated after review as it not useful in production
    '''
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


def password_reset_done(request):
    '''
    Display nessary html after reset is done.
    .. deprecated::  0.1.0
    '''
    return Response({'password has been changes'},
                    status=204)


def change_password(request, uidb64, token):
    '''
    Display nessary html after reset is done.
    .. deprecated:: 0.1.0
    '''
    return render(request, 'account/password_rest_confirm_form.html')


def change_password_done(requests):
    '''
    Display nessary html after reset is done.
    .. deprecated:: 0.1.0
    '''
    return render(requests, 'account/password_rest_done.html')
