from django.db import models
from core.models import AbstractBase, House
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from twilio.rest import TwilioRestClient

class Issue(AbstractBase):
    title = models.CharField(max_length=255)
    house = models.ForeignKey(House)
    room = models.ForeignKey(Room, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.TextField(max_length=65535)
    creation_date = models.DateField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolution_date = models.DateField()


class IssueComment(AbstractBase):
    issue = models.ForeignKey(Issue)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
