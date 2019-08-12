from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from myapp.models import LeaveRequest, WorkFromHome, UserProfile
from myapp.permissions import IsOwnerOnly, UserCreatePermission
from myapp.serializers import LeaveRequestSerializer, WFHRequestSerializer, UserSerializer


class LeaveRequestViewSets(ModelViewSet):
    serializer_class = LeaveRequestSerializer
    permission_classes = (IsOwnerOnly, IsAuthenticated)
    authentication_classes = [TokenAuthentication]
    filter_backends = (SearchFilter,)
    search_fields = ('requested_date', 'is_approved')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        annual_leave=self.request.user.current_year_detail()
                    )

    def get_queryset(self):
        return LeaveRequest.objects.filter(user=self.request.user)


class WorkFromHOmeCreate(LeaveRequestViewSets):
    queryset = WorkFromHome.objects.all()
    serializer_class = WFHRequestSerializer


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserCreatePermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('email', 'first_name', 'groups', 'department_name')
    authentication_classes = [TokenAuthentication]


class UserLogin(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



