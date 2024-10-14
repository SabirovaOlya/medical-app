from django.urls import path

from apps.users.views import UserListCreateView, ProfileListCreateView, HospitalListCreateView, PharmacyListCreateView, \
    ClientListCreateView, DoctorListCreateView

urlpatterns = [
    path('user/', UserListCreateView.as_view(), name='user_list'),
    path('profile/', ProfileListCreateView.as_view(), name='profile_list'),
    path('hospital/', HospitalListCreateView.as_view(), name='hospital_list'),
    path('pharmacy/', PharmacyListCreateView.as_view(), name='pharmacy_list'),
    path('doctor/', DoctorListCreateView.as_view(), name='doctor_list'),
    path('client/', ClientListCreateView.as_view(), name='client_list'),
]
