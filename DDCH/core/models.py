from django.db import models
from django.contrib.auth import AbstractUser
import uuid


class AbstractBase(models):
    id = models.CharField(max_length=36, editable=False)

    def __init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


class House(AbstractBase):
    name = models.CharField(max_length=100)
    postcode = models.CharField(max_length=7)


class User(AbstractUser):
    house = models.ForeignKey(House)
