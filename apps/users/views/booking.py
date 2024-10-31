from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.users.models import Booking
from apps.users.serializers import BookingSerializer, BookingDetailSerializer


@extend_schema(tags=['Booking List'])
class BookingListCreateView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


@extend_schema(tags=['Booking Detail'])
class BookingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer

    def perform_update(self, serializer):
        serializer.save()
