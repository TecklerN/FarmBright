from pathlib import Path
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# ---------------------------------------------------------
# TRAINING EXAMPLES
# ---------------------------------------------------------

training_data = [
    # Crop recommendation
    ("which crop should I plant", "crop_recommendation"),
    ("what crop is suitable for my farm", "crop_recommendation"),
    ("what should I grow in my area", "crop_recommendation"),
    ("which small grain should I plant", "crop_recommendation"),
    ("recommend a crop for my field", "crop_recommendation"),
    ("what crop can grow well here", "crop_recommendation"),
    ("which grain is best for this location", "crop_recommendation"),

    # Seed query
    ("what seed should I use", "seed_query"),
    ("which seed variety is recommended", "seed_query"),
    ("what seeds can I plant", "seed_query"),
    ("recommend a seed variety", "seed_query"),
    ("which sorghum seed should I use", "seed_query"),
    ("what pearl millet seed is suitable", "seed_query"),

    # Fertilizer query
    ("how much fertilizer do I need", "fertilizer_query"),
    ("what fertilizer should I use", "fertilizer_query"),
    ("which fertilizer is suitable", "fertilizer_query"),
    ("how much fertilizer for my field", "fertilizer_query"),
    ("what fertilizer should I use for sorghum", "fertilizer_query"),

    # Water query
    ("how much water does the crop need", "water_query"),
    ("how much water will I need", "water_query"),
    ("what are the water requirements", "water_query"),
    ("how much water does sorghum need", "water_query"),
    ("does pearl millet need a lot of water", "water_query"),

    # Planting time
    ("when should I plant", "planting_time"),
    ("when is the best time to plant", "planting_time"),
    ("what is the planting season", "planting_time"),
    ("when should I plant sorghum", "planting_time"),
    ("when should I plant millet", "planting_time"),
]


texts = [item[0] for item in training_data]
labels = [item[1] for item in training_data]


# ---------------------------------------------------------
# MACHINE LEARNING NLP PIPELINE
# ---------------------------------------------------------

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# Train the model
model.fit(texts, labels)


# ---------------------------------------------------------
# SAVE MODEL
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "nlp_model.joblib"

joblib.dump(model, MODEL_PATH)

print("NLP model trained successfully.")
print(f"Model saved to: {MODEL_PATH}")