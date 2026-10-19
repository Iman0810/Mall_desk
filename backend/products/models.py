from django.db import models

class Product(models.Model):
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    #restricted field for internal use
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    internal_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"