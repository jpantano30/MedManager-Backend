from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationViewSet, UserViewSet, MyTokenObtainPairView, MyTokenRefreshView, MedicationLogViewSet, index

router = DefaultRouter()
router.register(r'medications', MedicationViewSet)
router.register(r'medication_logs', MedicationLogViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('', include(router.urls)),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
]
