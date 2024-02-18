from rest_framework import serializers
from tripscan.models import TripScan

class TripScanSerializerr(serializers.ModelSerializer):
    class Meta:
        model=TripScan
        fields="__all__"
        read_only_fields=['uuid']
        