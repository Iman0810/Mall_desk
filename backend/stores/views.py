from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import StoreMembership
from accounts.serializers import StoreMembershipSerializer

#return the list of stores the logged-in user belongs to
class UserStoresView(APIView):
    def get(self, request):
        memberships = StoreMembership.objects.filter(user=request.user).select_related("store")
        data = [{"id": m.store.id, "name": m.store.name, "role": m.role} for m in memberships]
        return Response(data)