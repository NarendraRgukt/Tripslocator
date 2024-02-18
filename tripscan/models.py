from django.db import models
import uuid


class TripScan(models.Model):
    uuid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    name=models.CharField(max_length=150)
    latitude=models.TextField()
    longitude=models.TextField()
    time=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
