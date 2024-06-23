from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationViewSet, UserViewSet, MyTokenObtainPairView, MyTokenRefreshView

router = DefaultRouter()
router.register(r'medications', MedicationViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
]
