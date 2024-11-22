from apps.users.views.auth import SignUpAPIView, LoginAPIView
from apps.users.views.booking import BookingListCreateView, BookingRetrieveUpdateDestroyView
from apps.users.views.clients import ClientListCreateView, ClientsRetrieveUpdateDestroyView
from apps.users.views.doctors import DoctorListCreateView, DoctorRetrieveUpdateDestroyView
from apps.users.views.hospitals import HospitalListCreateView, HospitalRetrieveUpdateDestroyView
from apps.users.views.pharmacies import PharmacyListCreateView, PharmaciesRetrieveUpdateDestroyView
from apps.users.views.profiles import ProfileListView, ProfileCreateView
from apps.users.views.reset_password import SendResetEmailAPIView, VerifyEmailCodeAPIView, ResetPasswordAPIView
from apps.users.views.users import UserListView
