from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from apps.users.models import Profile
from apps.users.serializers import ProfileModelSerializer


@extend_schema(tags=['Profiles'])
class ProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer
