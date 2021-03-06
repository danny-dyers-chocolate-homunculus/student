from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.contenttypes import generic
import uuid
import hashlib


class AbstractBase(models.Model):

    """
    AbstractBase class for handling setting id's and
    setting creation dates of objects.

    """
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def view_count(self):
        """
        Returns an integer of how many views the current object has.
        """
        model_type = generic.ContentType.objects.get_for_model(self)
        count = ViewLog.objects.filter(content_type__pk=model_type.id,
                                       object_id=self.id).count()
        return count

    class Meta:
        abstract = True


class House(AbstractBase):
    """
    A house that multiple users are attached to.
    """
    name = models.CharField(max_length=100)
    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="house_landlord")
    postcode = models.CharField(max_length=7)
    rooms = models.IntegerField()
    landlord = models.OneToOneField('User', blank=True, null=True, related_name='landlord_user')
    #Rent per annum
    rpa = models.FloatField()

    def __unicode__(self):
        return "%s: %s" % (self.postcode, self.name)

    # def get_house_balance(self):
    #     bills = Bill.objects.filter(house=self.user.house)

    #     balance = 0

    #     for bill in bills:
    #         for payment in bill.billpayment_set.all():
    #             balance =+ payment.amount_due - payment.amount_paid


class User(AbstractUser, AbstractBase):
    house = models.ForeignKey(House, blank=True, null=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    landlord = models.BooleanField(default=False)

    GRAVATAR_URL = "http://www.gravatar.com/avatar/"
    ROBOHASH_URL = "http://robohash.org/"

    def _get_email_hash(self):
        h = hashlib.md5()
        h.update(self.email)
        return h.hexdigest()

    @property
    def profile_picture(self):
        return ("%s%s?d=%s%s.png&s=200") % (self.GRAVATAR_URL,
                                            self._get_email_hash(),
                                            self.ROBOHASH_URL,
                                            self._get_email_hash())

    @property
    def monthly_rent(self):
        """
        Returns the users monthly rent cost.
        """
        return self.house.rpa/self.house.rooms


    def get_balance(self):
        from bills.models import Bill, BillPayment
        payments = BillPayment.objects.filter(user=self)

        balance = 0

        for payment in payments:
            balance += payment.amount_due - payment.amount_paid

        return balance



class Post(AbstractBase):
    text = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    parent_post = models.ForeignKey('self', blank=True, null=True)

    @property
    def is_comment(self):
        if self.parent_post:
            return True
        else:
            return False

    @property
    def type(self):
        if self.parent_post:
            return self.Type.COMMENT
        else:
            return self.Type.POST

    def __unicode__(self):
        return "%s: %s" % (self.type, self.text[0:50])

    class Type:
        POST = "post"
        COMMENT = "comment"

    class Meta:
        ordering = ['-date_created']


class ViewLog(AbstractBase):

    """
    Used for keeping track of view counts of objects. Uses a generic relation
    to be used with any model type. This should be implemented in other apps views.
    """
    logged_object = generic.GenericForeignKey('content_type', 'object_id')
    object_id = models.CharField(max_length=36)
    content_type = models.ForeignKey(generic.ContentType)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def log(cls, model_instance, user):
        """
        classmethod for creating a new view log for the current supplied instance.

        @param model_instance The instance of the object to log.
        @param User The User that viewed the object.
        @return ViewLog returns the newly created ViewLog instance.
        """
        view = cls()
        view.logged_object = model_instance
        view.user = user
        view.save()
        return view


class contact(AbstractBase):
    name = models.CharField(max_length=255)
    house = models.ForeignKey(House)
    phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    notes = models.TextField(max_length=65535, blank=True, null=True)
