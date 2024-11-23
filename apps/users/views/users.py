from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from apps.users.models import User
from apps.users.permission import IsSuperuser
from apps.users.serializers import UserModelSerializer


@extend_schema(tags=['Users List'])
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsSuperuser]
