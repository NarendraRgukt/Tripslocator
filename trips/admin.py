from django.contrib import admin

from trips import models

admin.site.register(models.Trip)
admin.site.register(models.TripDetails)
