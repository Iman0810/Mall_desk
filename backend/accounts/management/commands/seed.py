from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from stores.models import Store
from accounts.models import StoreMembership
from products.models import Product

class Command(BaseCommand):
    help = "Seed the database with realistic test data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")
        
        get_user_model().objects.all().delete()
        Store.objects.all().delete()
        Product.objects.all().delete()

        # 1. Create Branches
        downtown = Store.objects.create(name="Downtown Flagship")
        airport = Store.objects.create(name="Airport Terminal 2")
        mall = Store.objects.create(name="Westfield Mall")

        User = get_user_model()
        
        # 2. Create Users
        ceo = User.objects.create_user(username="admin", password="password123", first_name="Sarah", last_name="Jenkins", email="sarah.j@malldesk.com")
        
        # Downtown Staff
        manager = User.objects.create_user(username="manager", password="password123", first_name="David", last_name="Chen", email="david.c@malldesk.com")
        staff = User.objects.create_user(username="staff", password="password123", first_name="Emily", last_name="Davis", email="emily.d@malldesk.com")
        
        # Westfield Staff
        west_mgr = User.objects.create_user(username="west_mgr", password="password123", first_name="Marcus", last_name="Johnson", email="marcus.j@malldesk.com")
        west_staff = User.objects.create_user(username="west_staff", password="password123", first_name="Tom", last_name="Smith", email="tom.s@malldesk.com")

        # Airport Staff
        air_mgr = User.objects.create_user(username="air_mgr", password="password123", first_name="Priya", last_name="Patel", email="priya.p@malldesk.com")
        air_staff = User.objects.create_user(username="air_staff", password="password123", first_name="Alex", last_name="Wong", email="alex.w@malldesk.com")

        # 3. Assign Roles
        # Sarah oversees all
        StoreMembership.objects.create(user=ceo, store=downtown, role="ADMIN")
        StoreMembership.objects.create(user=ceo, store=airport, role="ADMIN")
        StoreMembership.objects.create(user=ceo, store=mall, role="ADMIN")
        
        # Downtown
        StoreMembership.objects.create(user=manager, store=downtown, role="MANAGER")
        StoreMembership.objects.create(user=staff, store=downtown, role="STAFF")
        
        # Westfield
        StoreMembership.objects.create(user=west_mgr, store=mall, role="MANAGER")
        StoreMembership.objects.create(user=west_staff, store=mall, role="STAFF")

        # Airport
        StoreMembership.objects.create(user=air_mgr, store=airport, role="MANAGER")
        StoreMembership.objects.create(user=air_staff, store=airport, role="STAFF")

        # 4. Create Products (Electronics)
        Product.objects.create(store=downtown, name="Apple MacBook Pro 14\"", sku="AP-MBP14", price=1999.00, stock=5, cost_price=1500.00)
        Product.objects.create(store=downtown, name="Sony WH-1000XM5", sku="SN-XM5", price=399.00, stock=15, cost_price=250.00)
        Product.objects.create(store=downtown, name="Anker PowerCore 20000", sku="AN-PC20", price=49.99, stock=100, cost_price=20.00)
        
        Product.objects.create(store=airport, name="Bose QuietComfort Earbuds", sku="BS-QCE", price=279.00, stock=3, cost_price=180.00)
        Product.objects.create(store=airport, name="Apple iPad Mini", sku="AP-IPM", price=499.00, stock=10, cost_price=380.00)
        Product.objects.create(store=airport, name="Belkin Travel Adapter", sku="BK-TA1", price=29.99, stock=50, cost_price=10.00)

        Product.objects.create(store=mall, name="Samsung Galaxy S24", sku="SM-S24", price=899.00, stock=25, cost_price=650.00)
        Product.objects.create(store=mall, name="JBL Flip 6 Speaker", sku="JB-FL6", price=129.95, stock=40, cost_price=80.00)
        Product.objects.create(store=mall, name="Logitech MX Master 3", sku="LG-MXM3", price=99.00, stock=0, cost_price=60.00) # Sold out!

        self.stdout.write(self.style.SUCCESS("Successfully seeded database with a realistic store structure!"))