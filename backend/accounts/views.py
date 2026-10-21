from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.exceptions import PermissionDenied
from accounts.permissions import require_role
from .models import User, StoreMembership
from .serializers import StoreMembershipSerializer
from django.contrib.auth import get_user_model

class LoginView(APIView):
    permission_classes = [AllowAny] # Anyone can attempt to log in

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)
            
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        })

class StoreUserListView(APIView):
    def get(self, request, store_id):
        # Admin and Manager can view users
        store, _ = require_role(request.user, store_id, ["ADMIN", "MANAGER"])
        memberships = StoreMembership.objects.filter(store=store).select_related("user")
        return Response(StoreMembershipSerializer(memberships, many=True).data)

class StoreUserAssignView(APIView):
    def post(self, request, store_id):
        # Allow both Admin and Manager to assign users
        store, membership = require_role(request.user, store_id, ["ADMIN", "MANAGER"])
        
        username = request.data.get("username")
        role = request.data.get("role")
        
        if not username or not role:
            return Response({"error": "Username and role required"}, status=400)
            
        # SECURITY CHECK 1: Managers cannot create Admins
        if role == "ADMIN" and membership.role != "ADMIN":
            return Response({"error": "Only Administrators can create other Admins."}, status=403)
            
        User = get_user_model()
        user = User.objects.filter(username=username).first()
        
        if user:
            # SECURITY CHECK 2: Managers cannot steal/transfer users from other stores
            existing_memberships = StoreMembership.objects.filter(user=user).exclude(store=store)
            if existing_memberships.exists() and membership.role != "ADMIN":
                return Response(
                    {"error": f"User '{username}' already belongs to another branch. Only an Administrator can transfer them."}, 
                    status=403
                )
        else:
            # Create the user if they don't exist
            clean_name = username.replace('.', ' ').replace('_', ' ').title()
            name_parts = clean_name.split()
            first_name = name_parts[0] if name_parts else username
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else "Employee"
            
            user = User.objects.create_user(
                username=username, 
                password="password123",
                first_name=first_name,
                last_name=last_name,
                email=f"{username.lower()}@malldesk.com"
            )
            
        store_membership, created = StoreMembership.objects.update_or_create(
            user=user, store=store,
            defaults={"role": role}
        )
        return Response(StoreMembershipSerializer(store_membership).data, status=201 if created else 200)