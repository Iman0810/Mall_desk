from tests.base import BaseAPITestCase
from rest_framework import status
from accounts.models import StoreMembership

class RolePermissionTests(BaseAPITestCase):
    def test_staff_cannot_create_product(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(f"/api/stores/{self.city_center.id}/products/", {
            "name": "Hacker Item", "sku": "HACK-1", "price": 5
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_cannot_assign_users(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(f"/api/stores/{self.city_center.id}/users/assign/", {
            "username": "outsider_test", "role": "STAFF"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_cannot_transfer_user_from_another_store(self):
        
        StoreMembership.objects.create(user=self.outsider, store=self.airport, role="STAFF")
        
        self.client.force_authenticate(user=self.manager) 
        
        
        response = self.client.post(f"/api/stores/{self.city_center.id}/users/assign/", {
            "username": "outsider_test", "role": "STAFF"
        })
        
      
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)