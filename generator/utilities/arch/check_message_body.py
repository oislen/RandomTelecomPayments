from fastapi import  HTTPException

def check_message_body(body: dict):
    if not body.get("n_users"):
        raise HTTPException(status_code=400, detail="'n_users' field is required")