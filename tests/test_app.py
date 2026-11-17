import unittest
from app import app
from risk_engine import assess_slope, validate_payload

GOOD = {
 "rain_1h_mm":12,"rain_24h_mm":78,"rain_72h_mm":155,"slope_deg":31,
 "soil_moisture_pct":62,"landcover_disturbance":0.4,
 "geology_susceptibility":3,"drainage_impairment":3,"past_landslide":0
}
class TerraGuardTests(unittest.TestCase):
 def setUp(self): self.client=app.test_client()
 def test_health(self):
  r=self.client.get('/api/health'); self.assertEqual(r.status_code,200); self.assertEqual(r.json['status'],'ok')
 def test_assessment(self):
  r=self.client.post('/api/assess',json=GOOD); self.assertEqual(r.status_code,200); self.assertIn('score',r.json['result'])
 def test_validation(self):
  bad=dict(GOOD);bad['slope_deg']=120
  r=self.client.post('/api/assess',json=bad);self.assertEqual(r.status_code,400)
 def test_demo_sites(self):
  r=self.client.get('/api/demo-sites');self.assertEqual(r.status_code,200);self.assertEqual(len(r.json['sites']),5)
 def test_assistant(self):
  r=self.client.post('/api/ask',json={'question':'What are warning signs?'})
  self.assertEqual(r.status_code,200);self.assertIn('cracks',r.json['answer'].lower())
if __name__=='__main__':unittest.main()
