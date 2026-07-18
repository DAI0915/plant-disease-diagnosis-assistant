import json

def load_disease_database(path="data/plantvillage_disease_database.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_class_name(class_name):
    plant, disease = class_name.split("___")
    
    plant = plant.replace("_", " ")
    disease = disease.replace("_", " ")
    
    return plant, disease


def build_diagnosis(disease_database, result):
    class_name = result["class_name"]
    confidence = result["confidence"]
    
    plant, disease = parse_class_name(class_name)
    info = disease_database.get(class_name)
    
    if info is None:
        return {
            "plant": plant,
            "disease": disease,
            "confidence": confidence,
            "message": "Detailed disease information is not available."
        }
    
    return {
        "plant": plant,
        "disease": disease,
        "confidence": confidence,
        "symptoms": info["symptoms"],
        "cause": info["cause"],
        "treatment": info["treatment"],
        "prevention": info["prevention"]
    }


def generate_explanation(diagnosis):
    symptoms = "\n".join(
        f"- {item}"
        for item in diagnosis["symptoms"]
    )

    treatment = "\n".join(
        f"- {item}"
        for item in diagnosis["treatment"]
    )

    prevention = "\n".join(
        f"- {item}"
        for item in diagnosis["prevention"]
    )

    return f"""
    Predicted plant: {diagnosis["plant"]}
    Predicted condition: {diagnosis["disease"]}
    Confidence: {diagnosis["confidence"] * 100:.2f}%
    
    Typical symptoms:
    {symptoms}
    
    Cause:
    {diagnosis["cause"]}

    Recommended actions:
    {treatment}

    Prevention:
    {prevention}

    This result is generated from an image-classification model and should not be treated as a definitive professional diagnosis.
    """.strip()
