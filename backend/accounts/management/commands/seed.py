from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from stores.models import Store
from accounts.models import StoreMembership
from products.models import Product

class Command(BaseCommand):
    help = "Seed the database with test data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")
        
        # clear existing data 
        get_user_model().objects.all().delete()
        Store.objects.all().delete()
        Product.objects.all().delete()

        # create Stores (Branches)
        city_center = Store.objects.create(name="City Center Branch")
        airport = Store.objects.create(name="Airport Branch")

        # create users
        admin = get_user_model().objects.create_user(username="admin", password="password123", email="admin@test.com")
        manager = get_user_model().objects.create_user(username="manager", password="password123")
        staff = get_user_model().objects.create_user(username="staff", password="password123")
        multi = get_user_model().objects.create_user(username="multi", password="password123")

        
        # admin in both branches
        StoreMembership.objects.create(user=admin, store=city_center, role="ADMIN")
        StoreMembership.objects.create(user=admin, store=airport, role="ADMIN")
        
        # manager in city center only
        StoreMembership.objects.create(user=manager, store=city_center, role="MANAGER")
        
        # staff in city center only
        StoreMembership.objects.create(user=staff, store=city_center, role="STAFF")
        
        # Multi: Manager in City Center, Staff in Airport
        StoreMembership.objects.create(user=multi, store=city_center, role="MANAGER")
        StoreMembership.objects.create(user=multi, store=airport, role="STAFF")

        # Create Products (Distinct for isolation testing)
        Product.objects.create(store=city_center, name="City Center Shirt", sku="CC-001", price=20.00, stock=50, cost_price=10.00)
        Product.objects.create(store=city_center, name="City Center Hat", sku="CC-002", price=15.00, stock=5, cost_price=5.00)
        
        Product.objects.create(store=airport, name="Airport Pants", sku="AP-001", price=40.00, stock=20, cost_price=20.00)
        Product.objects.create(store=airport, name="Airport Socks", sku="AP-002", price=5.00, stock=100, cost_price=2.00)

        self.stdout.write(self.style.SUCCESS("Successfully seeded database!"))