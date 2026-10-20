from tests.base import BaseAPITestCase
from rest_framework import status

class AssistantIsolationTests(BaseAPITestCase):
    def test_assistant_only_uses_active_store_data(self):
        self.client.force_authenticate(user=self.manager) # Manager only has Downtown access
        
        response = self.client.post(f"/api/stores/{self.downtown.id}/assistant/", {
            "message": "How many products do I have?"
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reply = response.data["reply"]
        
        # The mock assistant says: "I found X products... Here are a few: [names]"
        # Downtown has 1 product. Uptown has 1. It should say 1 product, and mention "DT Item"
        self.assertIn("1 products", reply)
        self.assertIn("DT Item", reply)
        self.assertNotIn("UT Item", reply) # CRITICAL: Must not leak Uptown data