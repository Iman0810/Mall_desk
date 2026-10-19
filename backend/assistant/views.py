from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import get_active_store
from products.models import Product

class AssistantChatView(APIView):
    def post(self, request, store_id):
        # 1. Enforce store isolation
        store, _ = get_active_store(request.user, store_id)
        
        message = request.data.get("message", "").lower()
        
        # 2. Fetch ONLY this store's products
        products = Product.objects.filter(store=store)
        
        # 3. Deterministic mock response
        if "product" in message or "inventory" in message or "how many" in message:
            count = products.count()
            names = ", ".join([p.name for p in products[:3]])
            reply = f"I found {count} products in {store.name}. Here are a few: {names}."
        elif "stock" in message or "low" in message:
            low_stock = products.filter(stock__lt=10)
            reply = f"There are {low_stock.count()} products with low stock in {store.name}."
        else:
            reply = f"Hello! I am the assistant for {store.name}. Ask me about products or stock."
            
        return Response({"reply": reply})