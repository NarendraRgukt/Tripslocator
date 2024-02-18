from django.contrib import admin
from roles import models

# Register your models here.
class OrganizationAdmin(admin.ModelAdmin):
    list_display=['uuid','name']

class RoleAdmin(admin.ModelAdmin):
    list_display=['uuid','name']

admin.site.register(models.Member)
admin.site.register(models.Organization,OrganizationAdmin)
admin.site.register(models.Role,RoleAdmin)
