from django.db import models
from core import AbstractBase
from django.contrib.contenttypes import generic
from django.conf import settings

# Create your models here.


class AbstractBill(AbstracBase):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(min_value=0, max_digits=8, decimal_places=2)
    creator = models.ForeignKey(user.AUTH_USER_MODEL)
    creation_date = models.DateField(auto_now_add=True)

    class Meta():
        abstract = True


class FixedBill(AbstractBill):
    due_date = models.DateField()


class RecurringBill(AbstractBill):
    due_date = models.DateField()


class BillPayment(AbstractBase):
    bill = generic.GenericForeignKey('content_type', 'object_id')
    object_id = models.CharField(max_length=36)
    content_type = models.ForeignKey(ContentType)
