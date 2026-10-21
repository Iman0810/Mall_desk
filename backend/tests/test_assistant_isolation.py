from tests.base import BaseAPITestCase
from rest_framework import status

class AssistantIsolationTests(BaseAPITestCase):
    def test_assistant_only_uses_active_store_data(self):
        self.client.force_authenticate(user=self.manager) 
        
        response = self.client.post(f"/api/stores/{self.city_center.id}/assistant/", {
            "message": "How many products do I have?"
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reply = response.data["reply"]
        
        self.assertIn("1 products", reply)
        self.assertIn("CC Item", reply)
        self.assertNotIn("AP Item", reply)

   
    def test_assistant_blocks_access_to_unauthorized_store(self):
        self.client.force_authenticate(user=self.manager) 
        
       
        response = self.client.post(f"/api/stores/{self.airport.id}/assistant/", {
            "message": "How many products do I have?"
        })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)