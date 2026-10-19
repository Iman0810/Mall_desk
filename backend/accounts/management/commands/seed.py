from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from stores.models import Store
from accounts.models import StoreMembership
from products.models import Product

class Command(BaseCommand):
    help = "Seed the database with test data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")
        
        # 1. Clear existing data (for easy re-running)
        get_user_model().objects.all().delete()
        Store.objects.all().delete()
        Product.objects.all().delete()

        # 2. Create Stores
        downtown = Store.objects.create(name="Downtown Store")
        uptown = Store.objects.create(name="Uptown Store")

        # 3. Create Users
        admin = get_user_model().objects.create_user(username="admin", password="password123", email="admin@test.com")
        manager = get_user_model().objects.create_user(username="manager", password="password123")
        staff = get_user_model().objects.create_user(username="staff", password="password123")
        multi = get_user_model().objects.create_user(username="multi", password="password123")

        # 4. Create Memberships (Roles)
        # Admin: Admin in both
        StoreMembership.objects.create(user=admin, store=downtown, role="ADMIN")
        StoreMembership.objects.create(user=admin, store=uptown, role="ADMIN")
        
        # Manager: Manager in Downtown only
        StoreMembership.objects.create(user=manager, store=downtown, role="MANAGER")
        
        # Staff: Staff in Downtown only
        StoreMembership.objects.create(user=staff, store=downtown, role="STAFF")
        
        # Multi: Manager in Downtown, Staff in Uptown
        StoreMembership.objects.create(user=multi, store=downtown, role="MANAGER")
        StoreMembership.objects.create(user=multi, store=uptown, role="STAFF")

        # 5. Create Products (Distinct for isolation testing)
        Product.objects.create(store=downtown, name="Downtown Shirt", sku="DT-001", price=20.00, stock=50, cost_price=10.00)
        Product.objects.create(store=downtown, name="Downtown Hat", sku="DT-002", price=15.00, stock=5, cost_price=5.00)
        
        Product.objects.create(store=uptown, name="Uptown Pants", sku="UT-001", price=40.00, stock=20, cost_price=20.00)
        Product.objects.create(store=uptown, name="Uptown Socks", sku="UT-002", price=5.00, stock=100, cost_price=2.00)

        self.stdout.write(self.style.SUCCESS("Successfully seeded database!"))