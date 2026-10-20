from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from stores.models import Store
from accounts.models import StoreMembership
from products.models import Product

class BaseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
       
        self.city_center = Store.objects.create(name="City Center Branch")
        self.airport = Store.objects.create(name="Airport Branch")

        User = get_user_model()
        self.admin = User.objects.create_user(username="admin_test", password="pw")
        self.manager = User.objects.create_user(username="manager_test", password="pw")
        self.staff = User.objects.create_user(username="staff_test", password="pw")
        self.outsider = User.objects.create_user(username="outsider_test", password="pw")

        
        StoreMembership.objects.create(user=self.admin, store=self.city_center, role="ADMIN")
        StoreMembership.objects.create(user=self.admin, store=self.airport, role="ADMIN")
        
        # managor and staff have access to only City Center
        StoreMembership.objects.create(user=self.manager, store=self.city_center, role="MANAGER")
        StoreMembership.objects.create(user=self.staff, store=self.city_center, role="STAFF")
        
     

        # renamed product variables
        self.cc_product = Product.objects.create(
            store=self.city_center, name="CC Item", sku="CC-1", price=10, cost_price=5
        )
        self.ap_product = Product.objects.create(
            store=self.airport, name="AP Item", sku="AP-1", price=20, cost_price=10
        )