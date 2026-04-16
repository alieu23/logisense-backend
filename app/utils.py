import joblib

model = None
vectorizer = None

def load_model():
    global model, vectorizer
    model = joblib.load("app/model/lr_model.joblib")
    vectorizer = joblib.load("app/model/vectorizer.joblib")



LABEL_MAP = {
    0: "negative",
    4: "positive"
}

def predict_sentiment(text: str):
    if model is None or vectorizer is None:
        raise Exception("Model and vectorizer must be loaded before prediction.")
    
    transformed= vectorizer.transform([text])
    
    prediction = model.predict(transformed)[0]
    return LABEL_MAP.get(prediction, "unknown")