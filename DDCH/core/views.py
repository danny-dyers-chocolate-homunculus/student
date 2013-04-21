# Create your views here.
from django.contrib.auth.views import login
from django.shortcuts import redirect, render
from core.models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, template_name='core/login.html')


class DashboardView(ListView):
    """
    ListView for displaying the list of current Cases.
    """
    model = Post
    template_name = "core/dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)
