from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# support for custom User models in Django 1.5+
from djangoratings.compat import get_username_field

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

from djangoratings.managers import VoteManager, SimilarUserManager


class Vote(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="votes")
    object_id = models.PositiveIntegerField()
    key = models.CharField(max_length=32)
    score = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        null=True, related_name="votes")
    ip_address = models.GenericIPAddressField()
    cookie = models.CharField(max_length=32, blank=True, null=True)
    date_added = models.DateTimeField(default=now, editable=False)
    date_changed = models.DateTimeField(default=now, editable=False)

    objects = VoteManager()

    content_object = GenericForeignKey()

    class Meta:
        unique_together = (('content_type', 'object_id', 'key', 'user', 'ip_address', 'cookie'), )

    def __str__(self):
        return u"%s voted %s on %s" % (self.user_display, self.score, self.content_object)

    def save(self, *args, **kwargs):
        self.date_changed = now()
        super(Vote, self).save(*args, **kwargs)

    def user_display(self):
        if self.user:
            return "%s (%s)" % (getattr(self.user, get_username_field()), self.ip_address)
        return self.ip_address

    user_display = property(user_display)

    def partial_ip_address(self):
        ip = self.ip_address.split('.')
        ip[-1] = 'xxx'
        return '.'.join(ip)

    partial_ip_address = property(partial_ip_address)


class Score(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    key = models.CharField(max_length=32)
    score = models.IntegerField()
    votes = models.PositiveIntegerField()

    content_object = GenericForeignKey()

    class Meta:
        unique_together = (('content_type', 'object_id', 'key'),)

    def __str__(self):
        return u"%s scored %s with %s votes" % (self.content_object, self.score, self.votes)



class SimilarUser(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="similar_users")
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="similar_users_from")
    agrees = models.PositiveIntegerField(default=0)
    disagrees = models.PositiveIntegerField(default=0)
    exclude = models.BooleanField(default=False)

    objects = SimilarUserManager()

    class Meta:
        unique_together = (('from_user', 'to_user'),)

    def __str__(self):
        return u"%s %s similar to %s" % (self.from_user, self.exclude and 'is not' or 'is', self.to_user)



class IgnoredObject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey()

    class Meta:
        unique_together = (('content_type', 'object_id'),)

    def __str__(self):
        return self.content_object
