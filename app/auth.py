from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()

COGNITO_REGION = "us-east-2"
USER_POOL_ID = "us-east-2_u7s949C4b"

def verify_token(credentials=Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.get_unverified_claims(token)
        groups = payload.get("cognito:groups", [])
        return {
            "user_id": payload.get("sub"),
       
            "groups": groups

        }
    except:
        raise HTTPException(status_code=401, detail="Invalid token")