"""Small, transparent FAQ assistant; no external LLM/API key is required."""
import re

KNOWLEDGE = [
    (["what is a landslide", "define landslide", "meaning of landslide"],
     "A landslide is the movement of rock, debris or earth down a slope under gravity. It can involve falls, topples, slides, spreads or flows. Water, geology, slope shape, earthquakes and human activity can influence slope failure."),
    (["why do landslides happen", "causes", "cause of landslide"],
     "Landslides usually result from interacting factors: steep or weakened slopes, weak rock/soil, water entering the ground, intense or prolonged rainfall, earthquakes, river or coastal erosion, excavation, deforestation and poorly managed drainage. No single factor guarantees failure."),
    (["warning signs", "early signs", "signs of landslide", "how to identify"],
     "Possible warning signs include new ground or road cracks, bulging ground, fresh seepage or muddy water, tilting trees or poles, leaning retaining walls, doors/windows suddenly sticking, and unusual sounds or movement. Report signs to local authorities and seek qualified assessment."),
    (["what should i do", "safety", "during a landslide", "evacuate"],
     "If you believe a slope is failing, move away from the path of moving debris if you can do so safely, warn others, and contact local emergency/disaster-management authorities. Follow official evacuation instructions. Do not approach the slope to take photographs. If you are in immediate danger, contact local emergency services."),
    (["rainfall threshold", "how much rain", "rain trigger"],
     "There is no single rainfall threshold that works for every slope. Thresholds depend on geology, soil depth, land cover, antecedent wetness, storm duration, local climate and monitoring quality. TerraGuard's rainfall scaling is only a demonstration reference, not an official trigger threshold."),
    (["soil moisture", "soil wet", "saturation", "why does water matter", "water affect slope", "pore-water", "pore water"],
     "As soil becomes wetter, pore-water pressure can rise and effective strength may decrease, depending on soil and drainage conditions. A single soil-moisture percentage is not universally comparable across sensors or soil types; calibration and sensor placement matter."),
    (["slope angle", "slope degree", "steepness"],
     "Slope angle is one terrain factor. Steeper slopes can have greater gravitational driving forces, but slope angle alone cannot predict failure. Rock strength, layering, water, vegetation, cuts, toe erosion and drainage also matter."),
    (["susceptibility", "hazard", "risk difference"],
     "Susceptibility describes where landslides are more likely based on terrain and environmental conditions. Hazard adds the likelihood, timing and magnitude of an event. Risk considers consequences to people, buildings, roads and services, combining hazard with exposure and vulnerability."),
    (["how score", "calculate", "weights", "model work", "algorithm"],
     "TerraGuard normalizes seven indicator groups to 0–100 and combines them with illustrative weights: rainfall 25%, slope 15%, soil moisture 20%, land-cover disturbance 10%, geology 10%, drainage impairment 10%, and past landslide evidence 10%. The result is a relative screening index, not a probability or validated ML prediction."),
    (["accuracy", "trained", "machine learning", "real ai", "real model"],
     "The current deployed engine is an explainable weighted screening model, not a trained machine-learning predictor. A defensible ML model needs verified landslide and non-landslide examples, consistent feature measurements, spatial/temporal holdout testing, calibration and expert review. We do not claim accuracy without that evidence."),
    (["data sources", "gsi", "nasa", "dataset"],
     "The project is designed to integrate India's Geological Survey of India (GSI) landslide inventory and susceptibility resources, NRSC/ISRO Landslide Atlas, NASA Global Landslide Catalog, NASA GPM IMERG rainfall and a suitable DEM such as SRTM/NASADEM. Always record product version, date, resolution, coverage and licence/usage conditions."),
    (["types of landslide", "types", "fall slide flow", "kinds of landslide"],
     "Common movement types include falls (material detaches and drops), topples (forward rotation), slides (movement along a surface; rotational or translational), lateral spreads (sideways extension, often involving liquefaction-sensitive material), and flows (soil/debris moves like a fluid). Real events can combine more than one movement type."),
    (["prevent landslide", "prevention", "mitigation", "reduce risk"],
     "Risk reduction is site-specific. Measures may include professionally designed surface and subsurface drainage, avoiding uncontrolled slope cuts or loading, maintaining suitable vegetation, protecting the slope toe, monitoring cracks and seepage, and enforcing land-use planning. Do not attempt structural work without qualified geotechnical design."),
    (["monitoring", "sensors", "monitor a slope", "inclinometer"],
     "Professional monitoring can combine rainfall gauges, soil-moisture or pore-pressure sensors, inclinometers, GNSS/GPS survey points, crack gauges, piezometers, remote sensing and field inspections. Sensor placement, calibration, data transmission, maintenance and alert thresholds must be designed for the site."),
    (["dem", "digital elevation", "terrain data", "srtm"],
     "A digital elevation model (DEM) represents ground elevation. Derivatives such as slope, aspect, curvature and drainage networks can support susceptibility mapping. Resolution, vegetation/building artefacts, coordinate reference systems and vertical accuracy affect the derived features."),
    (["inventory", "landslide catalogue", "event records"],
     "A landslide inventory records observed events and attributes such as location, date, movement type, trigger, size and impacts. It is essential for model development, but reporting gaps and mapping biases must be documented. A model also needs credible non-landslide samples, not only event points."),
    (["deforestation", "vegetation", "land cover"],
     "Vegetation can help stabilize some shallow soils through root reinforcement and can influence infiltration and runoff. Removing vegetation, cutting slopes or changing drainage may increase susceptibility in some settings, but the effect depends on local geology, soil, rainfall and engineering."),
    (["what does high mean", "risk level", "score meaning"],
     "The bands LOW, GUARDED, ELEVATED and HIGH SCREENING CONCERN are prototype categories created for this demonstration. They are not official warning levels. A low score does not prove a slope is safe, and a high score does not confirm a landslide will occur.")
]

def answer_question(question, assessment=None):
    q = re.sub(r"\s+", " ", question.lower()).strip()
    if assessment and any(w in q for w in ["my result", "this result", "my score", "why this", "explain my"]):
        try:
            score = assessment.get("score", "not available")
            level = assessment.get("risk_level", "not available")
            drivers = assessment.get("top_drivers", [])
            return f"Your last screening result was {score}/100 ({level}). Main contributing indicators: {', '.join(drivers) if drivers else 'not available'}. This is a relative screening index, not a probability. Review the indicator chart and seek local expert/official guidance for real sites."
        except AttributeError:
            pass
    for keywords, answer in KNOWLEDGE:
        if any(k in q for k in keywords):
            return answer
    return ("I can help with landslide causes, warning signs, rainfall triggers, soil moisture, slope angle, "
            "susceptibility versus hazard versus risk, model weights, score interpretation and data sources. "
            "Try asking: 'Why do landslides happen?' or 'How does the model calculate my score?'")
