from rest_framework.serializers import ModelSerializer

from apps.users.models import Booking
from apps.users.serializers import DoctorModelSerializer


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'doctor', 'reason', 'status', 'payment_status', 'consultation_fee', 'admin_fee', 'total']
        read_only_fields = ['id', 'date', 'time', 'status', 'payment_status', 'consultation_fee', 'admin_fee', 'total']


class BookingDetailSerializer(ModelSerializer):
    doctor = DoctorModelSerializer()

    class Meta:
        model = Booking
        fields = ['doctor', 'date', 'time', 'reason', 'status', 'payment_status']
        read_only_fields = ['id', 'date', 'time', 'status', 'payment_status']
