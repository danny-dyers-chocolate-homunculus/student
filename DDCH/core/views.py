# Create your views here.
from django.contrib.auth import login
from django.shortcuts import redirect


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, template_name='core/login.html')
