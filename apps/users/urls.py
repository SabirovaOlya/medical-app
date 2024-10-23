from django.urls import path

from apps.users.views import UserListCreateView, ProfileListCreateView, HospitalListCreateView, PharmacyListCreateView, \
    ClientListCreateView, DoctorListCreateView, SendEmailAPIView, VerifyEmailAPIView, LoginAPIView

urlpatterns = [
    path('user/', UserListCreateView.as_view(), name='user_list'),
    path('profile/', ProfileListCreateView.as_view(), name='profile_list'),
    path('hospital/', HospitalListCreateView.as_view(), name='hospital_list'),
    path('pharmacy/', PharmacyListCreateView.as_view(), name='pharmacy_list'),
    path('doctor/', DoctorListCreateView.as_view(), name='doctor_list'),
    path('client/', ClientListCreateView.as_view(), name='client_list'),
    path('send-email/', SendEmailAPIView.as_view(), name='send_email'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('login', LoginAPIView.as_view(), name='login')
]
