from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from accounts.permissions import get_active_store, require_role
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(APIView):
    def get(self, request, store_id):
        store, _ = get_active_store(request.user, store_id)
        products = Product.objects.filter(store=store)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, store_id):
        store, membership = require_role(request.user, store_id, ["ADMIN", "MANAGER"])
        
        if membership.role != "ADMIN" and ("cost_price" in request.data or "internal_notes" in request.data):
            return Response({"error": "You do not have permission to set restricted fields."}, status=403)

        serializer = ProductSerializer(data=request.data, context={"request": request, "membership": membership})
        if serializer.is_valid():
            serializer.save(store=store)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# ADD THIS CLASS BACK:
class ProductDetailView(APIView):
    @transaction.atomic
    def patch(self, request, store_id, pk):
        store, membership = require_role(request.user, store_id, ["ADMIN", "MANAGER"])
        
        product = Product.objects.filter(store=store, pk=pk).first()
        if not product:
            return Response({"error": "Not found"}, status=404)

        serializer = ProductSerializer(
            product, 
            data=request.data, 
            partial=True, 
            context={"request": request, "membership": membership}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)