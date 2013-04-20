# Create your views here.
from django.contrib.auth.views import login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required



def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, template_name='core/login.html')


@login_required
def dashboard(request):
  	return render(request, 'core/dashboard.html')