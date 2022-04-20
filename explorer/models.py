import uuid

from django.db import models


# NOTE: it is better to have dates of creation/modification for all imporant models
class TimestampedModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class CollectionModel(TimestampedModel):
    # NOTE: this is to avoid enumeration of records (but not really a problem here...)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
