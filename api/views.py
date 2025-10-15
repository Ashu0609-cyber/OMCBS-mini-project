from rest_framework import generics, permissions
from .serializers import UserCreationSerializer, MyTokenObtainPairSerializer, PatientProfileSerializer,DoctorProfileSerializer,HospitalSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsPatientUser,IsDoctorUser,IsHospitalAdminUser

class UserCreationView(generics.CreateAPIView):
    """
    API view for the first step of user registration.
    Accepts role, email, and password to create a basic user account.
    """
    serializer_class = UserCreationSerializer
    permission_classes = [permissions.AllowAny]



class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for token creation that uses our custom serializer.
    """
    # This line is the key. We are telling the view to use our new serializer.
    serializer_class = MyTokenObtainPairSerializer



class PatientProfileView(generics.CreateAPIView):
    # This view will use our new serializer.
    serializer_class = PatientProfileSerializer
    
    # This is the security guard! It checks permissions before running any logic.
    # IsAuthenticated: Checks if a valid token was provided.
    # IsPatientUser: Our custom rule that checks if the user's role is 'patient'.
    permission_classes = [permissions.IsAuthenticated, IsPatientUser]

    def perform_create(self, serializer):
        # This method is called just before saving the new profile.
        # We automatically link the new profile to the currently logged-in user.
        # This prevents a patient from accidentally creating a profile for someone else.
        serializer.save(user=self.request.user)

class DoctorProfileView(generics.CreateAPIView):
    # This view uses our new doctor serializer.
    serializer_class = DoctorProfileSerializer
    
    # This is our security guard. It requires a valid token AND the 'doctor' role.
    permission_classes = [permissions.IsAuthenticated, IsDoctorUser]

    def perform_create(self, serializer):
        # Automatically link the new profile to the currently logged-in doctor.
        serializer.save(user=self.request.user)
class HospitalCreationView(generics.CreateAPIView):
    # This view uses our new hospital serializer.
    serializer_class = HospitalSerializer
    
    # This is our security guard. Requires a valid token AND the 'hospital_admin' role.
    permission_classes = [permissions.IsAuthenticated, IsHospitalAdminUser]

    def perform_create(self, serializer):
        # This custom logic runs after the serializer validates the data but before it saves.
        # It creates the hospital and then associates the currently logged-in admin user with it.
        hospital = serializer.save()
        hospital.admins.add(self.request.user)