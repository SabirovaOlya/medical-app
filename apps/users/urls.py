from django.urls import path

from apps.users.views import (
    HospitalListCreateView, PharmacyListCreateView,
    DoctorListCreateView, ClientListCreateView, SignUpAPIView, LoginAPIView, SendResetEmailAPIView,
    ResetPasswordAPIView, DoctorRetrieveUpdateDestroyView, VerifyEmailCodeAPIView, HospitalRetrieveUpdateDestroyView,
    PharmaciesRetrieveUpdateDestroyView, ClientsRetrieveUpdateDestroyView, UserListView, ProfileListView,
    ProfileCreateView, BookingListCreateView, BookingRetrieveUpdateDestroyView
)
from apps.users.views.pharmacy import ProductListView, ProductDetailView, CartItemListView, CartItemDetailView, \
    OrderListView, OrderDetailView, ProductCreateView
from apps.users.views.wallet import WalletCreateView, WalletListView

# from apps.users.views.pharmacy import (
#     ProductListView, ProductDetailView, CartItemListView, CartItemDetailView,
#     OrderListView, OrderDetailView
# )

urlpatterns = [
    # User and Profile URLs
    path('user/', UserListView.as_view(), name='user_list'),
    path('profile/', ProfileListView.as_view(), name='profile_list'),
    path('profile-create', ProfileCreateView.as_view(), name='profile_create'),

    # Hospital URLs
    path('hospital/', HospitalListCreateView.as_view(), name='hospital_list'),
    path('hospital/<int:pk>/', HospitalRetrieveUpdateDestroyView.as_view(), name='hospital_detail'),

    # Pharmacy URLs
    path('pharmacy/', PharmacyListCreateView.as_view(), name='pharmacy_list'),
    path('pharmacy/<int:pk>/', PharmaciesRetrieveUpdateDestroyView.as_view(), name='pharmacy_detail'),

    # Doctor URLs
    path('doctor/', DoctorListCreateView.as_view(), name='doctor_list'),
    path('doctor/<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view(), name='doctor_detail'),

    # Client URLs
    path('client/', ClientListCreateView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientsRetrieveUpdateDestroyView.as_view(), name='client_detail'),

    # Auth
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),

    # Password Reset
    path('send-email/', SendResetEmailAPIView.as_view(), name='send-email'),
    path('verify-email/', VerifyEmailCodeAPIView.as_view(), name='verify-email'),
    path('restore-password/', ResetPasswordAPIView.as_view(), name='restore-password'),

    # Booking URLs
    path('bookings/', BookingListCreateView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking_detail'),
    path('wallet/', WalletListView.as_view(), name='wallet_list'),
    path('wallet-create/', WalletCreateView.as_view(), name='wallet_list'),

    # Pharmacy E-Commerce URLs
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product-create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartItemListView.as_view(), name='cart_list'),
    path('cart/<int:pk>/', CartItemDetailView.as_view(), name='cart_detail'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]
