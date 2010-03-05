from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Rating(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey()
    rating = models.PositiveIntegerField()
    # Dates
    created_at = models.DateTimeField(default=datetime.now,
                                      help_text=_('Auto-filled when created.'))
    updated_at = models.DateTimeField(help_text=_('Auto-updated when saved.'))

    class Meta:
        verbose_name = _('rating')
        verbose_name_plural = _('ratings')

    def __unicode__(self):
        return '%s rated %s as %s' % (unicode(self.user),
                                      unicode(self.item),
                                      str(self.rating))

    def save(self, force_insert=False, force_update=False):
        self.updated_at = datetime.now()
        super(Rating, self).save(force_insert, force_update)

class Calculation(models.Model):
    content_type = models.ForeignKey(ContentType)
    item1_object_id = models.PositiveIntegerField()
    item2_object_id = models.PositiveIntegerField()
    item1 = generic.GenericForeignKey('content_type', 'item1_object_id')
    item2 = generic.GenericForeignKey('content_type', 'item2_object_id')
    freq = models.IntegerField(default=0)
    diff = models.FloatField(default=0.0)
