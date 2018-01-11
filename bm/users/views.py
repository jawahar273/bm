from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import requests as post_man
from django.shortcuts import render
from  allauth.account import views as allauth_views

from .models import User

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
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
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


def redirect_after_email_confirm(request):
    return render(request, 'account/after_email_validation_confirm.html')

def change_password(request, uidb64, token):
    return render(request, 'account/password_rest_confirm_form.html')

class LoginAfterPasswordChangeView(allauth_views.PasswordChangeView):
    template_name = 'account/password_rest_done.html'
    @property
    def success_url(self):
        return reverse_lazy('change_password_done')

login_after_password_change = LoginAfterPasswordChangeView.as_view()

def change_password_done(requests):
    return render(requests, 'account/password_rest_done.html')