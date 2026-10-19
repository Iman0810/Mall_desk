from django.contrib import admin
from django.urls import path
from stores.views import UserStoresView
from products.views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/stores/", UserStoresView.as_view(), name="user-stores"),
    path("api/stores/<int:store_id>/products/", ProductListCreateView.as_view(), name="product-list"),
    path("api/stores/<int:store_id>/products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]