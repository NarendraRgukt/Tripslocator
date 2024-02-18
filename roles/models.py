from django.db import models
from django.contrib.auth import get_user_model
import uuid

class Role(models.Model):
    role_choices=(
        ('admin','admin'),
        ('HR','HR'),
        ('member','member')
    )
    uuid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=15,choices=role_choices,unique=True)

    def __str__(self):
        return self.name

class Organization(models.Model):
    uuid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    name=models.CharField(max_length=245,unique=True)
    description=models.TextField()
    def __str__(self):
        return self.name


class Member(models.Model):
    uuid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='member')
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='member',unique=True)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    


