from pathlib import Path
import re
import joblib


# ---------------------------------------------------------
# LOAD TRAINED NLP MODEL
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "nlp_model.joblib"

model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------
# ENTITY EXTRACTION
# ---------------------------------------------------------

CROP_NAMES = {
    "sorghum": "sorghum",
    "pearl millet": "pearl_millet",
    "pearl millet": "pearl_millet",
    "millet": "pearl_millet",
    "finger millet": "finger_millet",
    "rapoko": "finger_millet",
}


def extract_crop(text):
    text_lower = text.lower()

    for name, value in CROP_NAMES.items():
        if name in text_lower:
            return value

    return None

def extract_area(text):
    text_lower = text.lower()

    # First handle numbers written as digits
    digit_pattern = r"(\d+(?:\.\d+)?)\s*(?:ha|hectares?|hectare)"
    match = re.search(digit_pattern, text_lower)

    if match:
        return float(match.group(1))

    # Handle common spoken numbers
    number_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
        "one hundred": 100,
        "two hundred": 200,
        "three hundred": 300,
        "four hundred": 400,
        "five hundred": 500,
        "six hundred": 600,
        "seven hundred": 700,
        "eight hundred": 800,
        "nine hundred": 900,
        "one thousand": 1000,
    }

    # Check larger phrases first
    for phrase, value in sorted(
        number_words.items(),
        key=lambda item: len(item[0]),
        reverse=True
    ):
        pattern = rf"\b{re.escape(phrase)}\s*(?:ha|hectares?|hectare)\b"

        if re.search(pattern, text_lower):
            return float(value)

    return None


def extract_entities(text):
    return {
        "crop": extract_crop(text),
        "farm_area_hectares": extract_area(text),
    }


# ---------------------------------------------------------
# MAIN NLP FUNCTION
# ---------------------------------------------------------

def process_farmer_query(text):

    if not text or not text.strip():
        return {
            "error": "Please enter a farming question."
        }

    text = text.strip()

    # Predict intent
    intent = model.predict([text])[0]

    # Prediction confidence
    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities)

    # Extract entities
    entities = extract_entities(text)

    return {
        "query": text,
        "intent": intent,
        "confidence": round(float(confidence), 3),
        "entities": entities,
    }