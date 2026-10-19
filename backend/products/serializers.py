from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "store", "name", "sku", "price", "stock", "cost_price", "internal_notes"]

    def validate(self, attrs):
        """
        THE CRITICAL RESTRICTED FIELDS CHECK.
        If a non-Admin tries to include restricted fields, we reject the whole request.
        """
        request = self.context.get("request")
        membership = self.context.get("membership")
        
        restricted_fields = {"cost_price", "internal_notes"}
        
        # If the user is not an ADMIN, and the request contains restricted fields
        if membership and membership.role != "ADMIN":
            if restricted_fields.intersection(attrs.keys()):
                raise PermissionDenied("You do not have permission to edit restricted fields.")
                
        return attrs