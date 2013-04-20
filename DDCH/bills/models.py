from django.db import models
from core.models import AbstractBase
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings

# Create your models here.


class AbstractBill(AbstractBase):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateField(auto_now_add=True)

    class Meta():
        abstract = True


class FixedBill(AbstractBill):
    due_date = models.DateField()


class RecurringBill(AbstractBill):
    WEEKLY = 'W'
    DAILY = 'D'
    MONTHLY = 'M'
    ANNUALLY = 'A'

    RECURANCE_CHOICES = (
        (WEEKLY, 'Weekly'),
        (DAILY, 'Daily'),
        (MONTHLY, 'Monthly'),
        (ANNUALLY, 'Annually'),
    )

    recurance = models.CharField(max_length=1,
                                 choices=RECURANCE_CHOICES,
                                 default=MONTHLY)
    start_date = models.DateField()


class BillPayment(AbstractBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    bill = generic.GenericForeignKey('content_type', 'object_id')
    object_id = models.CharField(max_length=36)
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=(
            models.Q(app_label='bills', model='recurringbill') |
            models.Q(app_label='bills', model='fixedbill')
        )
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)
