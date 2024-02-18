from django.db import models
import uuid
from roles.models import Organization,Member

# Create your models here.

class Trip(models.Model):
    status_choices=(
        ('created','created'),
        ('started','started'),
        ('ended','ended')
    )
    trip_choices=(
        ('self','self'),
        ('assigned','assigned')
    )
    priority_choices=(
        ('low','low'),
        ('medium','medium'),
        ('high','high'),
        ('urgent','urgent')
    )
    uuid=models.UUIDField(primary_key=True,unique=True,editable=False,default=uuid.uuid4)
    name=models.CharField(max_length=245,unique=True)
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE)
    start_location=models.JSONField()
    end_location=models.JSONField()
    status=models.CharField(choices=status_choices,max_length=15,default="created")
    trip_type=models.CharField(max_length=10,choices=trip_choices)
    priority=models.CharField(choices=priority_choices,max_length=18)
    assigned_to=models.ForeignKey(Member,on_delete=models.CASCADE,related_name="trip")


    def __str__(self):
        return f'{self.organization}"s trip'



class TripDetails(models.Model):
    uuid=models.UUIDField(primary_key=True,unique=True,editable=False,default=uuid.uuid4)
    trip=models.OneToOneField(Trip,on_delete=models.CASCADE,related_name="trip_detail")
    start_scan=models.ForeignKey("tripscan.TripScan",on_delete=models.SET_NULL,null=True,related_name="tripscan_start")
    end_scan=models.ForeignKey('tripscan.TripScan',on_delete=models.SET_NULL,null=True,related_name='tripscan_end')
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return str(self.trip)

