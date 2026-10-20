from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from stores.models import Store
from accounts.models import StoreMembership
from products.models import Product

class BaseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.downtown = Store.objects.create(name="Downtown")
        self.uptown = Store.objects.create(name="Uptown")

        User = get_user_model()
        self.admin = User.objects.create_user(username="admin_test", password="pw")
        self.manager = User.objects.create_user(username="manager_test", password="pw")
        self.staff = User.objects.create_user(username="staff_test", password="pw")
        self.outsider = User.objects.create_user(username="outsider_test", password="pw")

        # Admin has access both
        StoreMembership.objects.create(user=self.admin, store=self.downtown, role="ADMIN")
        StoreMembership.objects.create(user=self.admin, store=self.uptown, role="ADMIN")
        
        # Manager and Staff only have access to Downtown
        StoreMembership.objects.create(user=self.manager, store=self.downtown, role="MANAGER")
        StoreMembership.objects.create(user=self.staff, store=self.downtown, role="STAFF")
        
        # Outsider has NO access to Downtown

        self.dt_product = Product.objects.create(
            store=self.downtown, name="DT Item", sku="DT-1", price=10, cost_price=5
        )
        self.ut_product = Product.objects.create(
            store=self.uptown, name="UT Item", sku="UT-1", price=20, cost_price=10
        )