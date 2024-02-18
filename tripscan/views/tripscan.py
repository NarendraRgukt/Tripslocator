from django.shortcuts import render

from rest_framework import views,status,permissions,authentication
from rest_framework.response import Response
from roles.permissions import AdminPermission
from tripscan import serializers,models
from trips.models import Trip,TripDetails
import json
from geopy.distance import geodesic
from django.shortcuts import get_object_or_404
from tripscan.models import TripScan
from roles.models import Member
import haversine as hs
from haversine import Unit


class TripScanCreate(views.APIView):
    serializer_class=serializers.TripScanSerializerr
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]

    def post(self, request, uuid):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        latitude = serializer.validated_data.get('latitude')
        longitude = serializer.validated_data.get('longitude')
        user_location = (float(latitude), float(longitude))

        try:
            trip=Trip.objects.get(uuid=uuid)
            member=Member.objects.get(user=request.user)
            if not (trip.assigned_to==member):
                return Response({'message':'you do not have the permission to do the scan'},status=401)

            trip_detail, created = TripDetails.objects.get_or_create(trip=trip)
            trip_start_location = trip.start_location
            trip_end_location = trip.end_location
            start_location_tuple = tuple(float(value) for value in trip_start_location['latitude'])
            end_location_tuple = tuple(float(value) for value in trip_end_location['longitude'])

            
            
            if trip_detail.start_scan is None:
                distance_to_destination = hs.haversine(user_location, start_location_tuple,unit=Unit.METERS)
            elif(trip_detail.end_scan is None):
                distance_to_destination = hs.haversine(user_location, end_location_tuple,unit=Unit.METERS)
            else:
                return Response({'message':'No more scans'},status=400)
            
            if distance_to_destination > 100:
                
                return Response({'message': 'You are not at the destination'}, status=400)
            else:
                
                    trip_scan = TripScan.objects.create(**serializer.validated_data)
                    
                    if trip_detail.start_scan is None:
                        trip_detail.start_scan = trip_scan
                        trip.status="started"
                        trip.save()
                    else:
                        trip_detail.end_scan = trip_scan
                        trip.status="ended"
                        trip.save()
                    trip_detail.save()

 

        except Trip.DoesNotExist:
            return Response({'message': 'Trip is not found'}, status=404)

        return Response({'message': 'Scan recorded successfully'}, status=200)

            
                


