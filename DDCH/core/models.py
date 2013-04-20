from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.contenttypes import generic
import uuid


class AbstractBase(models.Model):
    id = models.CharField(max_length=36, primary_key=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(AbstractBase, self).__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

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
    name = models.CharField(max_length=100)
    postcode = models.CharField(max_length=7)


class User(AbstractUser, AbstractBase):
    house = models.ForeignKey(House, blank=True, null=True)


class Post(AbstractBase):
    text = models.TextField()
    posted_by = models.ForeignKey(settings.USER_AUTH_MODEL)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    post = models.ForeignKey(self, blank=True, null=True)

    @property
    def is_comment(self):
        if self.post:
            return True
        else:
            return False


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
