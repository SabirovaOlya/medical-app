from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView

from apps.users.models import DoctorCategory
from apps.users.permission import IsSuperuser, IsClient
from apps.users.serializers.doctors import DoctorCategoryModelSerializer


@extend_schema(tags=["Doctor Category List"])
class DoctorCategoryListView(ListAPIView):
    queryset = DoctorCategory.objects.all()
    serializer_class = DoctorCategoryModelSerializer
    permission_classes = [IsSuperuser | IsClient]


@extend_schema(tags=["Doctor Category Create"])
class DoctorCategoryCreateView(CreateAPIView):
    queryset = DoctorCategory.objects.all()
    serializer_class = DoctorCategoryModelSerializer
    permission_classes = [IsSuperuser]


# @extend_schema(tags=["Doctor Category Detail"])
# class DoctorCategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     queryset = DoctorCategory.objects.all()
#     serializer_class = DoctorCategoryModelSerializer
#     permission_classes = [IsSuperuser]
