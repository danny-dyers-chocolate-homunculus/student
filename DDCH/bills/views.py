from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from bills.models import *
from django.shortcuts import render
import pdb


def analyse_view(request):
    return render(request, "bills/analyse.html")


class ExpenseListView(ListView):
    model = Bill
    template_name = "bills/expenses.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ExpenseListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(ExpenseListView, self).get_queryset().filter(house=self.request.user.house)
        return queryset
