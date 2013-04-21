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
        if(self.recipient.phone):
            client = TwilioRestClient(settings.TWILLIO_ACCOUNT, settings.TWILLIO_TOKEN)
            message = client.sms.messages.create(
                to=self.recipient.phone, from_="+441827231000", body=self.message+" - from "+str(self.sender))
        super(Message, self).save()