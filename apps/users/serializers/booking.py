from rest_framework.serializers import ModelSerializer

from apps.users.models import Booking
from apps.users.serializers import DoctorModelSerializer


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'client', 'doctor', 'date', 'time', 'reason', 'status', 'payment_status']
        read_only_fields = ['id', 'status', 'payment_status']


class BookingDetailSerializer(ModelSerializer):
    doctor = DoctorModelSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'doctor', 'date', 'time', 'reason', 'consultation_price', 'status', 'payment_status']