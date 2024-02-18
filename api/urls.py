from django.urls import path
from account.views import auth
from roles.views import roles
from trips.views import trips
from tripscan.views import tripscan

urlpatterns = [
    path('user/token/',auth.UserTokenView.as_view(),name='user-token'),
    path('member/',roles.MembersGetPost.as_view(),name='member-get-post'),
    path('member/<uuid:uuid>/',roles.MemberUpdateDelete.as_view(),name='member-detail'),
    path('trips/',trips.TripCreateRetrieve.as_view(),name="trip-post-get"),
    path("trips/<uuid:uuid>/",trips.TripUpdateDelete.as_view(),name='trip-detail'),
    path("trips/<uuid:uuid>/scans/",tripscan.TripScanCreate.as_view(),name="trip-scan-create")
]
