from tests.base import BaseAPITestCase
from rest_framework import status

class CombinedUpdateTests(BaseAPITestCase):
    def test_manager_cannot_sneak_restricted_field(self):
        self.client.force_authenticate(user=self.manager)
        
        # Manager tries to update a valid field and restricted field 
        response = self.client.patch(f"/api/stores/{self.city_center.id}/products/{self.cc_product.id}/", {
            "name": "Hacked Name",
            "cost_price": 99.99
        })
        
        # The request must rejected entirely
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # The valid field must not saved
        self.cc_product.refresh_from_db()
        self.assertEqual(self.cc_product.name, "CC Item")
        self.assertEqual(self.cc_product.cost_price, 5.00)