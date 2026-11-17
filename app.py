from flask import Flask, render_template, request, jsonify
from risk_engine import assess_slope, validate_payload
from assistant import answer_question
from pathlib import Path
import csv

app = Flask(__name__)
ROOT = Path(__file__).resolve().parent

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "application": "TerraGuard AI", "version": "2.0"})

@app.post("/api/assess")
def assess():
    payload = request.get_json(silent=True) or {}
    errors = validate_payload(payload)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 400
    result = assess_slope(payload)
    return jsonify({"ok": True, "result": result})

@app.get("/api/demo-sites")
def demo_sites():
    path = ROOT / "data" / "demo_scenarios.csv"
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    results = []
    for row in rows:
        payload = {k: row[k] for k in (
            "rain_1h_mm", "rain_24h_mm", "rain_72h_mm", "slope_deg",
            "soil_moisture_pct", "landcover_disturbance", "geology_susceptibility",
            "drainage_impairment", "past_landslide"
        )}
        for k in payload:
            if k == "past_landslide":
                payload[k] = int(payload[k])
            else:
                payload[k] = float(payload[k])
        result = assess_slope(payload)
        result["site_name"] = row["site_name"]
        result["description"] = row["description"]
        result["inputs"] = payload
        results.append(result)
    return jsonify({"data_type": "synthetic_demo_scenarios", "sites": results})

@app.post("/api/ask")
def ask():
    body = request.get_json(silent=True) or {}
    question = str(body.get("question", "")).strip()
    context = body.get("assessment")
    if not question:
        return jsonify({"ok": False, "answer": "Please type a question first."}), 400
    return jsonify({"ok": True, "answer": answer_question(question, context)})

@app.get("/api/model-info")
def model_info():
    return jsonify({
        "model_name": "TerraGuard Explainable Slope Screening Engine",
        "model_type": "transparent weighted multi-indicator screening index",
        "trained_ml_model_available": False,
        "reason": "No verified, labelled local landslide and non-landslide training dataset was supplied.",
        "warning": "This academic screening prototype is not a calibrated probability, official forecast, or evacuation instruction."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= int(__import__("os").environ.get("PORT", 5000)), debug=False)
