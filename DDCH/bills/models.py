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
            super(Bill, self).save()
            user_set = self.house.user_set
            for user in user_set.all():
                bill_payment = BillPayment()
                bill_payment.user = user
                bill_payment.bill = self
                bill_payment.amount_due = float(self.amount) / len(user_set.all())
                bill_payment.save()

    def __unicode__(self):
        return "bill: "+self.title

class BillPayment(AbstractBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    bill = models.ForeignKey(Bill)

    amount_due = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    amount_paid = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    def __unicode__(self):
        return self.bill.title + " payment (by "+self.user.username+")"
