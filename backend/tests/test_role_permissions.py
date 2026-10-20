from tests.base import BaseAPITestCase
from rest_framework import status

class RolePermissionTests(BaseAPITestCase):
    def test_staff_cannot_create_product(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(f"/api/stores/{self.downtown.id}/products/", {
            "name": "Hacker Item", "sku": "HACK-1", "price": 5
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_cannot_assign_users(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post(f"/api/stores/{self.downtown.id}/users/assign/", {
            "username": "outsider_test", "role": "STAFF"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)