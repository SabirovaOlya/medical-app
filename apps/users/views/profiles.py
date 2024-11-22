from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from apps.users.models import Profile
from apps.users.permission import IsSuperuser
from apps.users.serializers import ProfileModelSerializer


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
