from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.models import User, Profile, Hospital, Pharmacy, Doctor, Client
from apps.users.serializers import UserModelSerializer, \
    ProfileModelSerializer, HospitalModelSerializer, PharmacyModelSerializer, DoctorModelSerializer, \
    ClientModelSerializer, LoginSerializer, SignUpSerializer


@extend_schema(tags=['Users'])
class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


# @extend_schema(tags=['Users'])
# class UserListCreateView(
#     mixins.ListModelMixin,  # Handles GET (list)
#     mixins.CreateModelMixin,  # Handles POST (create)
#     mixins.UpdateModelMixin,  # Handles PUT/PATCH (update)
#     GenericAPIView
# ):
#     queryset = User.objects.all()
#     serializer_class = UserModelSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)

@extend_schema(tags=['Profiles'])
class ProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer


@extend_schema(tags=['Hospitals'])
class HospitalListCreateView(ListCreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalModelSerializer


@extend_schema(tags=['Pharmacies'])
class PharmacyListCreateView(ListCreateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacyModelSerializer


@extend_schema(tags=['Doctors'])
class DoctorListCreateView(ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorModelSerializer


@extend_schema(tags=['Clients'])
class ClientListCreateView(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer


@extend_schema(tags=['Sign Up'])
class SignUpAPIView(GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        username = serializer.data['username']
        password = serializer.validated_data['password']

        user = User.objects.create(email=email, username=username, is_active=False)
        user.set_password(password)
        user.save()

        return Response({"message": "Success"})


@extend_schema(tags=['Login'])
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        return Response({"message": f"Login successful, welcome {username}"})

# class VerifyEmailAPIView(GenericAPIView):
#     serializer_class = VerifyEmailSerializer
#     permission_classes = [AllowAny]
# 
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
# 
#         email = serializer.validated_data['email']
#         code = serializer.validated_data['code']
# 
#         cached_code = cache.get(email)
# 
#         if cached_code is None:
#             raise ValidationError('No cached data found for this email.')
# 
#         if code != cached_code:
#             raise ValidationError('Code is incorrect.')
# 
#         # Activate the user
#         user = User.objects.filter(email=email).first()
#         if user:
#             user.is_active = True
#             user.save()
# 
#         return Response({"message": "Email verified, account activated successfully"})
