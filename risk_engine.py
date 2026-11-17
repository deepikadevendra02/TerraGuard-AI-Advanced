"""Explainable landslide screening engine.

Important: this is an educational, rule-based screening index, NOT a validated
landslide probability or an operational early-warning model. The reference
scales and weights below are illustrative and must be calibrated locally.
"""
WEIGHTS = {
    "rainfall": 0.25,
    "slope": 0.15,
    "soil_moisture": 0.20,
    "landcover": 0.10,
    "geology": 0.10,
    "drainage": 0.10,
    "history": 0.10,
}

REQUIRED_RANGES = {
    "rain_1h_mm": (0, 500),
    "rain_24h_mm": (0, 1500),
    "rain_72h_mm": (0, 3000),
    "slope_deg": (0, 90),
    "soil_moisture_pct": (0, 100),
    "landcover_disturbance": (0, 1),
    "geology_susceptibility": (1, 5),
    "drainage_impairment": (1, 5),
    "past_landslide": (0, 1),
}

def validate_payload(data):
    errors = []
    for key, (lo, hi) in REQUIRED_RANGES.items():
        if key not in data or data[key] in (None, ""):
            errors.append(f"{key} is required.")
            continue
        try:
            value = float(data[key])
        except (TypeError, ValueError):
            errors.append(f"{key} must be a number.")
            continue
        if not lo <= value <= hi:
            errors.append(f"{key} must be between {lo} and {hi}.")
    return errors

def _clamp(v):
    return max(0.0, min(100.0, v))

def assess_slope(data):
    """Return an explainable 0-100 relative screening index."""
    rain1 = float(data["rain_1h_mm"])
    rain24 = float(data["rain_24h_mm"])
    rain72 = float(data["rain_72h_mm"])
    slope = float(data["slope_deg"])
    moisture = float(data["soil_moisture_pct"])
    landcover = float(data["landcover_disturbance"])
    geology = float(data["geology_susceptibility"])
    drainage = float(data["drainage_impairment"])
    history = float(data["past_landslide"])

    # Demonstration scaling references only; not universal rainfall thresholds.
    rain_score = (
        0.25 * _clamp(rain1 / 30 * 100) +
        0.40 * _clamp(rain24 / 150 * 100) +
        0.35 * _clamp(rain72 / 300 * 100)
    )
    # Slope is a terrain factor, not a stand-alone failure predictor.
    slope_score = _clamp(slope / 45 * 100)
    moisture_score = _clamp(moisture)
    landcover_score = _clamp(landcover * 100)
    geology_score = _clamp((geology - 1) / 4 * 100)
    drainage_score = _clamp((drainage - 1) / 4 * 100)
    history_score = 100.0 if history >= 1 else 0.0

    indicators = {
        "Rainfall": round(rain_score, 1),
        "Slope": round(slope_score, 1),
        "Soil moisture": round(moisture_score, 1),
        "Land-cover disturbance": round(landcover_score, 1),
        "Geological susceptibility": round(geology_score, 1),
        "Drainage impairment": round(drainage_score, 1),
        "Past landslide evidence": round(history_score, 1),
    }
    score = round(
        rain_score * WEIGHTS["rainfall"] +
        slope_score * WEIGHTS["slope"] +
        moisture_score * WEIGHTS["soil_moisture"] +
        landcover_score * WEIGHTS["landcover"] +
        geology_score * WEIGHTS["geology"] +
        drainage_score * WEIGHTS["drainage"] +
        history_score * WEIGHTS["history"], 1
    )

    # Demonstration bands only; never treat as official alert thresholds.
    if score < 25:
        level, color = "LOW", "green"
    elif score < 45:
        level, color = "GUARDED", "yellow"
    elif score < 65:
        level, color = "ELEVATED", "orange"
    else:
        level, color = "HIGH SCREENING CONCERN", "red"

    drivers = sorted(indicators.items(), key=lambda item: item[1], reverse=True)
    strongest = [name for name, value in drivers[:3] if value >= 35]
    if not strongest:
        strongest = [drivers[0][0]]
    actions = {
        "LOW": [
            "Continue routine observation and keep surface drains clear.",
            "Avoid cutting into the slope or concentrating water onto it.",
            "Record new cracks, seepage, tilting trees or retaining-wall movement."
        ],
        "GUARDED": [
            "Increase observation during and after prolonged or intense rainfall.",
            "Check for blocked drains, fresh seepage, cracks and small slope movements.",
            "Share observations with local authorities or a qualified geologist."
        ],
        "ELEVATED": [
            "Arrange prompt field inspection by a qualified geologist or geotechnical engineer.",
            "Keep people away from visibly unstable ground and the runout path.",
            "Follow local district/SDMA advisories and prepare household communication."
        ],
        "HIGH SCREENING CONCERN": [
            "Treat this as a high-priority screening result requiring urgent expert verification.",
            "Stay away from cracks, bulges, flowing muddy water and the base of unstable slopes.",
            "Follow official district/SDMA instructions; do not use this score as an evacuation order."
        ]
    }[level]

    return {
        "score": score,
        "risk_level": level,
        "color": color,
        "indicator_scores": indicators,
        "top_drivers": strongest,
        "weights": {k: round(v * 100) for k, v in WEIGHTS.items()},
        "recommended_actions": actions,
        "interpretation": (
            f"The largest contributing indicators in this scenario are {', '.join(strongest)}. "
            "The score is a relative screening index based on the entered values, not a probability "
            "that a landslide will occur."
        ),
        "model_notice": (
            "Educational screening prototype. Weights and scaling references are illustrative, "
            "not locally calibrated. It cannot issue official warnings or guarantee safety."
        )
    }
