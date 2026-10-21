from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import get_active_store
from products.models import Product

from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import get_active_store
from products.models import Product

class AssistantChatView(APIView):
    def post(self, request, store_id):
        store, _ = get_active_store(request.user, store_id)
        message = request.data.get("message", "").lower()
        products = Product.objects.filter(store=store)
        
        reply = ""

        # Specific Brand/Product search
        if "nike" in message or "shoes" in message:
            nike_products = products.filter(name__icontains="nike")
            if nike_products.exists():
                reply = f"We have {nike_products.count()} Nike products. Example: {nike_products.first().name} for ${nike_products.first().price}."
            else:
                reply = f"I couldn't find any Nike products in {store.name}."

        elif "xiaomi" in message:
            xiaomi_products = products.filter(name__icontains="xiaomi")
            reply = f"We have {xiaomi_products.count()} Xiaomi items in {store.name}."

        # Sold out items
        elif "sold out" in message or "out of stock" in message:
            out_of_stock = products.filter(stock=0)
            if out_of_stock.exists():
                names = ", ".join([p.name for p in out_of_stock])
                reply = f"The following items are completely sold out: {names}."
            else:
                reply = "Great news! Nothing is currently sold out in this branch."

        # Low stock
        elif "low stock" in message or "running low" in message:
            low_stock = products.filter(stock__gt=0, stock__lt=5)
            if low_stock.exists():
                names = ", ".join([f"{p.name} (only {p.stock} left)" for p in low_stock])
                reply = f"You need to restock these: {names}."
            else:
                reply = "All products have healthy stock levels."

        # Generic inventory count
        elif "how many" in message or "inventory" in message or "products" in message:
            count = products.count()
            names = ", ".join([p.name for p in products[:3]])
            reply = f"There are {count} products in {store.name}. Top items: {names}."
            
        else:
            reply = f"Hello! I am the assistant for {store.name}. You can ask me about our products, stock levels, or if anything is sold out."

        return Response({"reply": reply})