from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.models import Profile
from apps.users.permission import IsSuperuser
from apps.users.serializers import ProfileModelSerializer
from apps.users.serializers.profiles import UserSelfInfoSerializer


@extend_schema(tags=['Profile list'])
class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer
    permission_classes = [IsSuperuser]


@extend_schema(tags=['Profile Create'])
class ProfileCreateView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['User Self Info'])
class UserSelfInfoView(RetrieveUpdateAPIView):
    serializer_class = UserSelfInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
