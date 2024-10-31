from django.urls import path

from apps.users.views import UserListCreateView, ProfileListCreateView, HospitalListCreateView, PharmacyListCreateView, \
    DoctorListCreateView, ClientListCreateView, SignUpAPIView, LoginAPIView, SendResetEmailAPIView, \
    ResetPasswordAPIView, DoctorRetrieveUpdateDestroyView, VerifyEmailCodeAPIView, HospitalRetrieveUpdateDestroyView, \
    PharmaciesRetrieveUpdateDestroyView, ClientsRetrieveUpdateDestroyView, BookingListCreateView, \
    BookingRetrieveUpdateDestroyView

urlpatterns = [
    path('user/', UserListCreateView.as_view(), name='user_list'),
    path('profile/', ProfileListCreateView.as_view(), name='profile_list'),
    # Hospital urls
    path('hospital/', HospitalListCreateView.as_view(), name='hospital_list'),
    path('hospital/<int:pk>/', HospitalRetrieveUpdateDestroyView.as_view(), name='hospital_detail'),
    # Pharmacy urls
    path('pharmacy/', PharmacyListCreateView.as_view(), name='pharmacy_list'),
    path('pharmacy/<int:pk>/', PharmaciesRetrieveUpdateDestroyView.as_view(), name='pharmacy_detail'),
    # Doctor urls
    path('doctor/', DoctorListCreateView.as_view(), name='doctor_list'),
    path('doctor/<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view(), name='doctor_detail'),
    # Client urls
    path('client/', ClientListCreateView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientsRetrieveUpdateDestroyView.as_view(), name='client_detail'),
    # Auth
    path('signup/', SignUpAPIView.as_view(), name='send_email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    # Restore password
    path('send-email/', SendResetEmailAPIView.as_view(), name='send-email'),
    path('verify-email/', VerifyEmailCodeAPIView.as_view(), name='verify-email'),
    path('restore-password/', ResetPasswordAPIView.as_view(), name='restore-password'),
    # Booking urls
    path('bookings/', BookingListCreateView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking_detail'),
]
