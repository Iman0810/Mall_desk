from tests.base import BaseAPITestCase
from rest_framework import status

class AssistantIsolationTests(BaseAPITestCase):
    def test_assistant_only_uses_active_store_data(self):
        self.client.force_authenticate(user=self.manager) # Manager only has City Center access
        
        response = self.client.post(f"/api/stores/{self.city_center.id}/assistant/", {
            "message": "How many products do I have?"
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reply = response.data["reply"]
        
        # City Center has 1 product (CC Item). Airport has 1.
        self.assertIn("1 products", reply)
        self.assertIn("CC Item", reply)
        self.assertNotIn("AP Item", reply) # 