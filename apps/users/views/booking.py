from datetime import datetime

from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from apps.users.models import Booking
from apps.users.serializers import BookingSerializer, BookingDetailSerializer


@extend_schema(tags=['Booking List'])
class BookingListCreateView(ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'client':
            return Booking.objects.filter(client=self.request.user.profile.client)
        return Booking.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, 'profile') or user.profile.role != 'client':
            raise ValidationError("Only clients can create bookings.")

        booking = serializer.save(
            client=user.profile.client,
            date=datetime.now().date(),
            time=datetime.now().time(),
            status='PENDING'
        )

        if self.process_payment(booking):
            booking.payment_status = True
            booking.status = 'CONFIRMED'
            booking.save()
        else:
            booking.status = 'CANCELLED'
            booking.save()
            raise ValidationError("Insufficient funds in wallet.")

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
    serializer_class = BookingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'client':
            return Booking.objects.filter(client=self.request.user.profile.client)
        return Booking.objects.none()

    def perform_update(self, serializer):
        serializer.save()
