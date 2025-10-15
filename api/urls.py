from django.urls import path
from .views import UserCreationView, MyTokenObtainPairView, PatientProfileView, DoctorProfileView,HospitalCreationView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # This URL is now for the initial, simple registration
    path('register/', UserCreationView.as_view(), name='user-register'),
    # NEW: This is your main login endpoint
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # NEW: This endpoint is used to get a new access token once the old one expires
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/patient/', PatientProfileView.as_view(), name='patient-profile-create'),
    path('profile/doctor/', DoctorProfileView.as_view(), name='doctor-profile-create'),
    path('profile/hospital/', HospitalCreationView.as_view(), name='hospital-profile-create'),
]
