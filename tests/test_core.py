import unittest
from risk_engine import assess_slope, validate_payload
from assistant import answer_question
GOOD={"rain_1h_mm":12,"rain_24h_mm":78,"rain_72h_mm":155,"slope_deg":31,"soil_moisture_pct":62,"landcover_disturbance":0.4,"geology_susceptibility":3,"drainage_impairment":3,"past_landslide":0}
class CoreTests(unittest.TestCase):
 def test_score_range(self):
  r=assess_slope(GOOD); self.assertGreaterEqual(r["score"],0); self.assertLessEqual(r["score"],100)
 def test_bad_range(self):
  d=dict(GOOD);d["slope_deg"]=99;self.assertTrue(validate_payload(d))
 def test_explanation(self):
  self.assertIn("pore-water",answer_question("Why does water matter?"))
 def test_contextual_answer(self):
  r=assess_slope(GOOD);self.assertIn("screening index",answer_question("Explain my score",r))
if __name__=="__main__":unittest.main()
