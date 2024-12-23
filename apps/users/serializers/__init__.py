from apps.users.serializers.doctors import DoctorModelSerializer, DoctorUpdateDeleteModelSerializer
from apps.users.serializers.auth import SignUpSerializer, LoginSerializer
from apps.users.serializers.booking import BookingSerializer, BookingDetailSerializer
from apps.users.serializers.clients import ClientModelSerializer, ClientUpdateDeleteModelSerializer
from apps.users.serializers.favorite import FavoriteProductSerializer
from apps.users.serializers.hospitals import HospitalModelSerializer, HospitalUpdateDeleteModelSerializer
from apps.users.serializers.pharmacies import PharmacyModelSerializer, PharmacyUpdateDeleteModelSerializer
from apps.users.serializers.pharmacy import ProductSerializer, CartItemSerializer, OrderItemSerializer, OrderSerializer
from apps.users.serializers.profiles import ProfileModelSerializer
from apps.users.serializers.reser_password import EmailModelSerializer, VerifyEmailSerializer, ResetPasswordSerializer
from apps.users.serializers.users import UserModelSerializer
from apps.users.serializers.wallet import WalletModelSerializer
