from django.db import models
from core.models import AbstractBase
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from twilio.rest import TwilioRestClient


class Message(AbstractBase):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="message_sender",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="message_recipient",
    )
    sent_date = models.DateField(auto_now_add=True)
    message = models.TextField(max_length=65535)
    read_date = models.DateField(null=True, blank=True)

    def save(self):
        account = "AC54e70c20c39d9c982827a1a7f5c926f4"
        token = "2732c9ae78b018ccaed3950da9531fa3"
        client = TwilioRestClient(account, token)
        super(Message, self).save()
