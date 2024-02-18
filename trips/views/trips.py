from django.shortcuts import render
from django.db.models import Q
from rest_framework import views,status,permissions,authentication
from rest_framework.response import Response
from trips import serializers
from trips.models import Trip,TripDetails
from roles.permissions import AdminPermission
from roles.models import Member


class TripCreateRetrieve(views.APIView):
    serializer_class=serializers.TripSerializer
    authentication_classes=[authentication.TokenAuthentication]
    
    def get_queryset(self):
        query=Q()
        status=self.request.GET.get('status')
        if status:
            query &=Q(status=status)
        trip_type=self.request.GET.get('trip_type')
        if trip_type:
            query &=Q(trip_type=trip_type)
        priority=self.request.GET.get('priority')
        if priority:
            query &=Q(priority=priority)
        assign_to=self.request.GET.get('assigned_to')
        if assign_to:
            query &=Q(assigned_to__uuid=assign_to)
        member=Member.objects.filter(user=self.request.user,role__name='admin')
        trip_name=self.request.GET.get('name')
        if trip_name:
            query &=Q(name__icontains=trip_name)
        if member.exists():
             queryset=Trip.objects.all()
        else:
            queryset=Trip.objects.filter(trip__assigned_to__member__user=self.request.user)
        return queryset.filter(query)
    def get_permission_classes(self):
        if self.request.method=="GET":
            return [permissions.IsAuthenticated()]
        else:
            return [AdminPermission()]
    
        
    def get(self,request,*args,**kwargs):
        member=Member.objects.filter(user=self.request.user).exists()
        serializer=self.serializer_class(self.get_queryset(),many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        assigned_to = serializer.validated_data.get('assigned_to')
        assigned_uuid = str(assigned_to.uuid) 
        member = Member.objects.get(user=request.user)
        
        if str(member.uuid) == assigned_uuid: 
            serializer.validated_data['trip_type'] = "self"
        
        serializer.save()
        
        return Response(serializer.data, status=201)
    
class TripUpdateDelete(views.APIView):
    serializer_class=serializers.TripSerializer
    permission_classes=[permissions.IsAuthenticated,AdminPermission]
    authentication_classes=[authentication.TokenAuthentication]

    def put(self,request,uuid):
        try:
            trip=Trip.objects.get(uuid=uuid)
            if trip.status!="created":
                return Response({'message':f'Trip {trip.status} already.You can not modify now'},status=403)
            serializer=self.serializer_class(trip,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=200)
        except Trip.DoesNotExist:
            return Response({'message':'Trip does not exist'},status=404)
        
    def delete(self,request,uuid):
        try:
            trip=Trip.objects.get(uuid=uuid)
            if trip.status!="created":
                return Response({'message':f'Trip {trip.status} already.You can not delete now'},status=403)
            trip.delete()
            return Response({'message':'Trip deleted successfully'},status=204)
        except Trip.DoesNotExist:
            return Response({'message':'Trip does not found'},status=404)
    