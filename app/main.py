from fastapi import Depends, FastAPI, HTTPException
from app.schemas import TextRequest
from app.utils import load_model, predict_sentiment
from fastapi.middleware.cors import CORSMiddleware
from app.auth import verify_token
import uuid
from datetime import datetime, timezone
from app.db import table

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def require_admin(user):
    if "admin" not in user["groups"]:
        raise HTTPException(status_code=403, detail="Admin access required")


@app.on_event("startup")
def startup_event():
    load_model()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/predict")
def predict(request: TextRequest, user=Depends(verify_token)):
    result = predict_sentiment(request.text)
    item = {
        "id": str(uuid.uuid4()),
        "userId": user.get("sub", "anonymous"),
        #"userId": user["sub"],
        "text": request.text,
        "sentiment": str(result),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    table.put_item(Item=item)

    return item

@app.get("/results")
def get_results():
    #require_admin(user)
    respose = table.scan()

    items = respose.get("Items", [])

    if "admin" in user["groups"]:
        return items    

    user_items = [
        item for item in items if item.get("userId") == user["user_id"]
    ]
    
    return user_items

@app.get("/admin")
def admin(user=Depends(verify_token)):
    require_admin(user)
    return {"message": "Welcome, admin!!!"}