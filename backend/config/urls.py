from django.contrib import admin
from django.urls import path
from stores.views import UserStoresView
from products.views import ProductListCreateView, ProductDetailView
from accounts.views import LoginView, StoreUserListView, StoreUserAssignView
from assistant.views import AssistantChatView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/stores/", UserStoresView.as_view(), name="user-stores"),
    path("api/stores/<int:store_id>/products/", ProductListCreateView.as_view(), name="product-list"),
    path("api/stores/<int:store_id>/products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("api/stores/<int:store_id>/users/", StoreUserListView.as_view(), name="store-user-list"),
    path("api/stores/<int:store_id>/users/assign/", StoreUserAssignView.as_view(), name="store-user-assign"),
    path("api/stores/<int:store_id>/assistant/", AssistantChatView.as_view(), name="assistant-chat"),
]