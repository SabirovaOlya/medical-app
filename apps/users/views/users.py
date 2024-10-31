from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from apps.users.models import User
from apps.users.serializers import UserModelSerializer


@extend_schema(tags=['Users'])
class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
