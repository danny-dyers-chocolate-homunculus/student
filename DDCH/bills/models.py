from django.db import models
from core.models import AbstractBase, House
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings

# Create your models here.


class Bill(AbstractBase):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    house = models.ForeignKey(House)
    creation_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

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
                                 default=MONTHLY,
                                 blank=True,
                                 )

    def save(self):
        if not self.id:
            user_set = self.house.user_set
            for user in user_set.all():
                bill_payment = BillPayment()
                bill_payment.user = user
                bill_payment.bill = self
                amount_due = self.amount / user_set.len()
        super(Bill, self).save()


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

    amount_due = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    amount_paid = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )
