from trips.models import Trip,TripDetails
from tripscan.models import TripScan
from rest_framework import serializers

class TripScanSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripScan
        fields = '__all__'


class TripDetailsSerializer(serializers.ModelSerializer):
    start_scan = TripScanSerializer()
    end_scan = TripScanSerializer()
    class Meta:
        model = TripDetails
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    trip_detail = TripDetailsSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields=['trip_detail']




