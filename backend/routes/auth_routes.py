from fastapi import APIRouter

from ..schemas import UserCreate
from ..database import get_db
from ..models import User
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import Form, HTTPException, Response
from ..database import supabase

router = APIRouter()

@router.post("/signup")
async def signup(email: str = Form(...), password: str = Form(...)):
    try:
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        if auth_response.user is None:
            raise HTTPException(status_code=400, detail="Failed to create user")
        return {
            "message": "User created successfully",
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "name": auth_response.user.user_metadata.get("name", "")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login(response: Response, email: str = Form(...), password: str = Form(...)):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if auth_response.user is None:
            raise HTTPException(status_code=400, detail="Failed to sign in")
        
        access_token = auth_response.session.access_token
        response.set_cookie(key='access_token', value=f"Bearer {access_token}", httponly=True)
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "name": auth_response.user.user_metadata.get("name", "")
            }
        }
        
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=400, detail="Invalid email or password")

@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}