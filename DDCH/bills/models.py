from django.db import models
from core import AbstractBase
from django.conf import settings

# Create your models here.


class FixedBill(AbstractBase):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(min_value=0, max_digits=8, decimal_places=2)
    user = models.ForeignKey(user.AUTH_USER_MODEL)
