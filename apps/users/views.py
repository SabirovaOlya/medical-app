from random import randint

from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response

from apps.users.models import User, Profile, Hospital, Pharmacy, Doctor, Client
from apps.users.serializers import EmailModelSerializer, VerifyEmailSerializer, UserModelSerializer, \
    ProfileModelSerializer, HospitalModelSerializer, PharmacyModelSerializer, DoctorModelSerializer, \
    ClientModelSerializer
from apps.users.tasks import send_to_email


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class ProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer


class HospitalListCreateView(ListCreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalModelSerializer


class PharmacyListCreateView(ListCreateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacyModelSerializer


class DoctorListCreateView(ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorModelSerializer


class ClientListCreateView(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer


class SendEmailAPIView(GenericAPIView):
    serializer_class = EmailModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        username = serializer.data['username']

        code = randint(1000, 9999)
        cache.set(email, {'code': code, 'username': username}, timeout=120)

        message = f"Your verification code is {code}"
        # send_to_email(message, email)
        send_to_email.delay(message, email)
        email = serializer.data['email']
        code = randint(1000, 9999)
        cache.set(email, code, timeout=120)

        message = f"Your verification code is {code}"
        send_to_email(message, email)

        print(f"Email: {email}, code: {code}")
        return Response({"message": "Code sent successfully"})


class VerifyEmailAPIView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        code = serializer.data['code']

        cached_data = cache.get(email)

        cached_code = cached_data.get('code')
        username = cached_data.get('username')

        if code != cached_code:
            raise ValidationError('Code is incorrect.')

        user = User.objects.filter(email=email).first()
        if user is None:
            user = User.objects.create(email=email, username=username)
            user.save()

        return Response({"message": "User added successfully"})
