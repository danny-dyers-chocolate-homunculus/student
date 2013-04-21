from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from bills.models import *
from django.shortcuts import render

def expense_view(request):
    return render(request, "bills/expenses.html")


def analyse_view(request):
    return render(request, "bills/analyse.html")
