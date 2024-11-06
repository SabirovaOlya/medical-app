from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.serializers import ValidationError

from apps.users.models import Booking
from apps.users.serializers import BookingSerializer, BookingDetailSerializer


@extend_schema(tags=['Booking List'])
class BookingListCreateView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save(status='PENDING')
        if self.process_payment(booking):
            booking.payment_status = True
            booking.status = 'CONFIRMED'
            booking.save()
        else:
            booking.status = 'CANCELLED'
            booking.save()
            raise ValidationError("Not enough money")

    def process_payment(self, booking):
        client_wallet = booking.client.user.user.wallet
        doctor_wallet = booking.doctor.user.user.wallet
        hospital_wallet = booking.doctor.hospital.user.user.wallet

        total_cost = booking.consultation_fee + booking.admin_fee

        if client_wallet.balance >= total_cost:
            client_wallet.balance -= total_cost
            client_wallet.save()

            doctor_wallet.balance += booking.consultation_fee
            doctor_wallet.save()

            hospital_wallet.balance += booking.admin_fee
            hospital_wallet.save()

            return True
        return False


@extend_schema(tags=['Booking Detail'])
class BookingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer

    def perform_update(self, serializer):
        serializer.save()
