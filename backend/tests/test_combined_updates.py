from tests.base import BaseAPITestCase
from rest_framework import status

class CombinedUpdateTests(BaseAPITestCase):
    def test_manager_cannot_sneak_restricted_field(self):
        self.client.force_authenticate(user=self.manager)
        
        # Manager try vto update a valid field (name) & a restricted field (cost_price)
        response = self.client.patch(f"/api/stores/{self.downtown.id}/products/{self.dt_product.id}/", {
            "name": "Hacked Name",
            "cost_price": 99.99
        })
        
        # The request must be rejected entirely
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # The valid field must NOT be saved
        self.dt_product.refresh_from_db()
        self.assertEqual(self.dt_product.name, "DT Item")
        self.assertEqual(self.dt_product.cost_price, 5.00)