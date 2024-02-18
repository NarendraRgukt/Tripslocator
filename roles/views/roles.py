from django.shortcuts import render
from roles import serializers,models
from roles.permissions import AdminPermission
from rest_framework import permissions,authentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model,authenticate
from django.db.models import Q,Value
from django.db.models.functions import Concat
from django.shortcuts import redirect
    
from rest_framework.views import APIView
import ast

class MembersGetPost(APIView):
    
    serializer_class=serializers.MemberUserSerializer
    permission_classes=[permissions.IsAuthenticated,AdminPermission]
    authentication_classes=[authentication.TokenAuthentication]

    def get_queryset(self):
        query=Q()
        role=self.request.GET.get('roles')
        if role:
            role=ast.literal_eval(role)
            query &=Q(role__uuid__in=role)
        fullname=self.request.GET.get('fullname')
        if fullname:
            print(fullname)
            q=Q(full_name__icontains=fullname)
            user_fullnames=get_user_model().objects.values('id','first_name','last_name').annotate(full_name=Concat('first_name',"last_name"))
            user_objects_filtered=user_fullnames.values('id').filter(full_name__icontains=fullname)
            query &=Q(user__id__in=user_objects_filtered)
            
        queryset=models.Member.objects.all()
        return queryset.filter(query)
    
    def get_serializer_class(self):
        if self.request.method=="GET":
            return serializers.MemberSerializer
        else:
            return self.serializer_class
    
    

    def get(self,request,*args,**kwargs):
        serializer_class = self.get_serializer_class() 
        serializer = serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request,*args,**kwargs):
        serializer_class=self.get_serializer_class()
        serializer=serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        organization = serializer.validated_data.get('organization')
        role = serializer.validated_data.get('role')
        first_name = serializer.validated_data.get('first_name')
        last_name= serializer.validated_data.get('last_name')
        user=authenticate(username=username,password=password)
        if user:
            member=models.Member.objects.create(user=user, organization=organization, role=role)
            return Response(serializer.data,status=status.HTTP_201_CREATED)


        user = get_user_model().objects.create_user(username=username, email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()

        member=models.Member.objects.create(user=user, organization=organization, role=role)
        member.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)
    


class MemberUpdateDelete(APIView):
    serializer_class=serializers.MemberSerializer
    permission_classes=[permissions.IsAuthenticated,AdminPermission]
    authentication_classes=[authentication.TokenAuthentication]

    def put(self,request,uuid):
        try:
            member=models.Member.objects.get(uuid=uuid)
            serializer=self.serializer_class(member,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)

        except models.Member.DoesNotExist:
            return Response({'message':'Member does not found'},status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request,uuid):
        try:
            member=models.Member.objects.get(uuid=uuid)
            user=get_user_model().objects.filter(member__uuid=member.uuid).first()
            member.delete()
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Member.DoesNotExist:
            return Response({'message':'member does not found'},status=status.HTTP_404_NOT_FOUND)

