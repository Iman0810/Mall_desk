from tests.base import BaseAPITestCase
from rest_framework import status

class StoreAccessTests(BaseAPITestCase):
    def test_outsider_cannot_view_products(self):
        self.client.force_authenticate(user=self.outsider)
        response = self.client.get(f"/api/stores/{self.city_center.id}/products/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_cannot_access_airport_products(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(f"/api/stores/{self.airport.id}/products/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)