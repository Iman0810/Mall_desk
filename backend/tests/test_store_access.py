from tests.base import BaseAPITestCase
from rest_framework import status

class StoreAccessTests(BaseAPITestCase):
    def test_outsider_cannot_view_products(self):
        self.client.force_authenticate(user=self.outsider)
        response = self.client.get(f"/api/stores/{self.downtown.id}/products/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_cannot_access_uptown_products(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(f"/api/stores/{self.uptown.id}/products/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)