from apps.users.views.auth import SignUpAPIView, LoginAPIView
from apps.users.views.booking import BookingListCreateView, BookingRetrieveUpdateDestroyView
from apps.users.views.clients import ClientListCreateView, ClientsRetrieveUpdateDestroyView
from apps.users.views.doctor_category import DoctorCategoryListView, DoctorCategoryCreateView
from apps.users.views.doctors import DoctorListView, DoctorRetrieveView
from apps.users.views.hospitals import HospitalListCreateView, HospitalRetrieveView
from apps.users.views.pharmacies import PharmacyListCreateView, PharmaciesRetrieveView
from apps.users.views.pharmacy import ProductListView, ProductCreateView, ProductDetailView, CartItemListView, \
    CartItemDetailView, OrderListView, OrderDetailView
from apps.users.views.profiles import ProfileListView, ProfileCreateView
from apps.users.views.reset_password import SendResetEmailAPIView, VerifyEmailCodeAPIView, ResetPasswordAPIView
from apps.users.views.users import UserListView
from apps.users.views.wallet import WalletListView, WalletCreateView
