# api/permissions.py

from rest_framework import permissions

class IsPatientUser(permissions.BasePermission):
   
    def has_permission(self, request, view):
        # This code checks two things:
        # 1. Is the user logged in? (request.user.is_authenticated)
        # 2. Is the user's role 'patient'? (request.user.role == 'patient')
        # Both must be true for permission to be granted.
        return request.user and request.user.is_authenticated and request.user.role == 'patient'
    

class IsDoctorUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # This rule checks if the user is logged in AND their role is 'doctor'.
        return request.user and request.user.is_authenticated and request.user.role == 'doctor'
class IsHospitalAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users with the 'hospital_admin' role.
    """
    def has_permission(self, request, view):
        # This rule checks if the user is logged in AND their role is 'hospital_admin'.
        return request.user and request.user.is_authenticated and request.user.role == 'hospital_admin'