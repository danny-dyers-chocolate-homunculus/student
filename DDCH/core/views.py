# Create your views here.
from django.contrib.auth.views import login
from django.shortcuts import redirect, render
from core.models import Post, House
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
import pdb
from django.core.exceptions import ImproperlyConfigured
<<<<<<< HEAD
<<<<<<< HEAD
=======
from django.contrib.auth.views import logout
from django.contrib import messages
>>>>>>> cb4f1edae2ba6949e8154cca7989864e2494d656
=======
from django.contrib.auth.views import logout
from django.contrib import messages
>>>>>>> cb4f1edae2ba6949e8154cca7989864e2494d656


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, template_name='core/login.html')


def custom_logout(request):
    if not request.user.is_authenticated():
        messages.add_message(request, messages.ERROR, 'No user logged in')
        return logout(request, next_page='/login')
    messages.add_message(request, messages.SUCCESS, 'Bye bye...')
    return logout(request, next_page='/login')


class DashboardView(ListView):
    """
    ListView for displaying the list of current Cases.
    """
    model = Post
    template_name = "core/dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if not self.request.user.house:
            raise ImproperlyConfigured("current user does not belong to a house")
        queryset = super(DashboardView, self).get_queryset().filter(posted_by__house=self.request.user.house)
        return queryset
