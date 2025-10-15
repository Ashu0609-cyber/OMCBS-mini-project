from rest_framework import serializers
# FIX: Add this import line
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, PatientProfile, DoctorProfile,Hospital
from django.db import transaction

# --- Serializer for Step 1: Initial User Creation ---
class UserCreationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})
        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        role = validated_data.get('role')
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role=role
        )
        return user


# --- Custom Serializer for the Login Response ---
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    This custom serializer adds a 'profile_complete' flag to the token payload.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        profile_complete = False
        if user.role == 'patient':
            profile_complete = hasattr(user, 'patientprofile')
        elif user.role == 'doctor':
            profile_complete = hasattr(user, 'doctorprofile')
        elif user.role == 'hospital_admin':
            profile_complete = True
            
        token['profile_complete'] = profile_complete
        token['role'] = user.role

        return token
class PatientProfileSerializer(serializers.ModelSerializer):
     class Meta:
        model = PatientProfile
        # We list the fields the user will submit.
        # We DON'T include the 'user' field, as the view will handle that automatically.
        fields = ['blood_group', 'emergency_contact_no', 'emergency_contact_relation', 'allergies', 'photo']
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        # We list all the fields a doctor will submit for their profile.
        # The 'user' field is handled automatically by the view.
        fields = [
            'specialization', 
            'qualification', 
            'experience_years', 
            'available_days', 
            'languages_spoken', 
            'hospital', 
            'photo'
        ]
class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        # List all the fields an admin will submit to create their hospital profile.
        # The 'admins' field will be handled by the view.
        fields = [
            'name', 
            'address', 
            'contact_no1', 
            'contact_no2', 
            'email', 
            'website',
            'license_no',
            'operating_hours',
            'num_departments',
            'photo'
        ]