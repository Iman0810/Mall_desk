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
        # ONLY Admin can assign users
        store, _ = require_role(request.user, store_id, ["ADMIN"])
        
        username = request.data.get("username")
        role = request.data.get("role")
        
        if not username or not role:
            return Response({"error": "Username and role required"}, status=400)
            
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error": "User not found"}, status=404)
            
        # Create or update the membership
        membership, created = StoreMembership.objects.update_or_create(
            user=user, store=store,
            defaults={"role": role}
        )
        return Response(StoreMembershipSerializer(membership).data, status=201 if created else 200)