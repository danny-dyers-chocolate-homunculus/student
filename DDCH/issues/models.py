from django.db import models
from core.models import AbstractBase, House, Post
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from twilio.rest import TwilioRestClient


class Issue(AbstractBase):
    title = models.CharField(max_length=255)
    house = models.ForeignKey(House)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.TextField(max_length=65535)
    creation_date = models.DateField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolution_date = models.DateField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            super(Issue, self).save()
            if not self.author.landlord and self.author.phone:
                client = TwilioRestClient(settings.TWILLIO_ACCOUNT, settings.TWILLIO_TOKEN)
                message = client.sms.messages.create(
                    to=self.house.landlord.phone, from_="+441827231000", body="Issue Raised: "+self.title+" on "+self.house.name)

            post = Post()
            post.text = "The issue '"+self.title+"' has been raised"
            post.posted_by = self.author
            post.save()

        if self.resolved:
            super(Issue, self).save()
            for user in self.house.user_set.all():
                if user.phone:
                    client = TwilioRestClient(settings.TWILLIO_ACCOUNT, settings.TWILLIO_TOKEN)
                    message = client.sms.messages.create(
                        to=user.phone, from_="+441827231000", body="The issue '"+self.title+"' has been resolved.")

            post = Post()
            post.text = "The issue '"+self.title+" has been resolved"
            post.posted_by = self.house.landlord
            post.save()
        else:
            super(Issue, self).save()

    def __unicode__(self):
        return self.title


class IssueComment(AbstractBase):
    issue = models.ForeignKey(Issue)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateField(auto_now_add=True)
    body = models.TextField(max_length=65535)
