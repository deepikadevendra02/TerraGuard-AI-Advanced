# TerraGuard AI — Interactive Landslide Intelligence Platform

**Problem reference:** SIH 2026 — SIH26001 (as supplied by the project team)

TerraGuard AI is an educational decision-support prototype for exploring how rainfall, slope, soil moisture, land-cover disturbance, geology, drainage and landslide history can influence a slope-screening index.

## What is included
- Responsive dashboard and interactive risk assessment form.
- Seven-indicator explainable weighted screening index.
- Indicator contribution chart and recommended verification actions.
- Five clearly labelled synthetic scenario examples.
- Built-in landslide knowledge assistant (no API key required).
- Flask JSON APIs: `/api/health`, `/api/assess`, `/api/demo-sites`, `/api/ask`, `/api/model-info`.
- Optional Random Forest training pipeline for a future verified labelled dataset.
- Render deployment configuration and basic API tests.

## Scientific integrity — read before presenting
The default engine is a **transparent weighted screening index**, not a trained machine-learning predictor, not a calibrated probability of failure, and not an official warning service. Its indicator weights, normalization reference values and category bands are illustrative. They must be locally calibrated and validated by qualified geologists/geotechnical specialists and competent authorities before any real-world use.

The included `data/demo_scenarios.csv` contains fictional teaching scenarios only. Do not use it to train or validate an ML model or claim predictive accuracy. A real ML model requires verified landslide AND non-landslide records with consistent features, location/time metadata, quality control, spatial/temporal holdout validation, calibration and expert review.

## Run locally (Windows)
1. Extract this ZIP.
2. Open the extracted `TerraGuard_AI_Complete` folder in VS Code.
3. Open Terminal → New Terminal.
4. Run:
```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```
5. Open `http://127.0.0.1:5000`.

## Upload updated code to your existing GitHub repository
Open terminal in the project folder:
```bash
git status
git add .
git commit -m "Upgrade TerraGuard AI interactive risk intelligence platform"
git push origin main
```
If Git says `nothing to commit`, check that you extracted the new files into the same folder that is connected to your Git repository. Do not run `git init` again if the folder already has `.git`.

## Deploy / redeploy on Render
This project includes `render.yaml`.
- New Web Service: select the GitHub repository and branch `main`.
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Health check path: `/api/health`
- Root directory: blank (unless you put the project inside a subfolder).
If an existing Render service is already connected to the repo, pushing a new commit normally triggers a redeploy. Check Render deploy logs and wait for status `Live`.

## API examples
### Health
`GET /api/health`

### Assessment
`POST /api/assess` JSON:
```json
{
  "rain_1h_mm": 12,
  "rain_24h_mm": 78,
  "rain_72h_mm": 155,
  "slope_deg": 31,
  "soil_moisture_pct": 62,
  "landcover_disturbance": 0.4,
  "geology_susceptibility": 3,
  "drainage_impairment": 3,
  "past_landslide": 0
}
```
### Ask a question
`POST /api/ask` JSON:
```json
{"question":"How does rainfall affect slope stability?"}
```
### Optional model training
Use only a real, documented labelled dataset with the columns in `data/training_template.csv`:
```bash
pip install -r requirements-ml.txt
python model_training.py --csv path/to/verified_landslide_dataset.csv
```
The target `landslide` must contain both 0 and 1. A `region_id` column enables a grouped region holdout. Without it, the script uses a random stratified split and warns that spatial leakage may remain. Review class balance, data provenance, spatial/temporal leakage, precision/recall, PR-AUC, calibration and expert acceptance before using any trained model. The optional model is not automatically connected to the production assessment API.

## Data sources for future integration
- Geological Survey of India landslide hazard resources: https://gsi.gov.in/landslide-hazard/
- NRSC/ISRO Landslide Atlas: https://www.nrsc.gov.in/nrscnew/resources_atlas_landslide.php
- NASA Global Landslide Catalog / hazard assessment: https://landslides.nasa.gov/
- NASA GPM IMERG rainfall: https://gpm.nasa.gov/data/imerg

## Important safety note
A low score does not prove a slope is safe. A high score does not prove failure is imminent. If you observe cracks, bulging ground, new seepage, tilting trees/poles or active slope movement, move away from danger if safe, notify local authorities and follow official instructions. Do not rely on this academic prototype for evacuation decisions.
