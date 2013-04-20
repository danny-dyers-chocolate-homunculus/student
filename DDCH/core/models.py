from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class AbstractBase(models.Model):
    id = models.CharField(max_length=36, primary_key=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(AbstractBase, self).__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

    class Meta:
        abstract = True


class House(AbstractBase):
    name = models.CharField(max_length=100)
    postcode = models.CharField(max_length=7)


class User(AbstractUser, AbstractBase):
    house = models.ForeignKey(House, blank=True, null=True)
