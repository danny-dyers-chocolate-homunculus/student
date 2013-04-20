from django.db import models
from core.models import AbstractBase
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings


class Message(AbstractBase):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    recipient = models.ForeignKey(settings.AUTH_MODEL_USER)
    sent_date = models.DateField(auto_now_add=True)
    message = models.TextField(max_length=65535)
    read_date = models.DateField()
