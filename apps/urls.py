from django.urls import path, include

urlpatterns = [
    path('pharmacy/', include('apps.pharmacy.urls', )),
    path('users/', include('apps.users.urls'))
]
