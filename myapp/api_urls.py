from django.urls import path, include
from rest_framework.routers import DefaultRouter

from myapp.api_views import LeaveRequestViewSets, WorkFromHOmeCreate, UserProfileViewSet, UserLogin

router = DefaultRouter()
router.register('leave_request_create', LeaveRequestViewSets, base_name='leave_request')
router.register('wfh_request_create', WorkFromHOmeCreate, base_name='wfh_request')
router.register('user_profile', UserProfileViewSet)

urlpatterns = [
    path('leave_request/', include(router.urls)),
    path('login/', UserLogin.as_view()),
]