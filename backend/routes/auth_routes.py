from fastapi import APIRouter, Form, HTTPException, Response, Depends, Request
from ..database import supabase
from ..auth import get_current_user, get_current_user_from_cookie

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
        response.set_cookie(key='access_token', value=f"Bearer {access_token}", httponly=False, secure=False, samesite='lax')
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid email or password")

@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", httponly=False, secure=False, samesite='lax')
    return {"message": "Logout successful"}

@router.get("/me")
async def get_me(request: Request):
    try:
        current_user = await get_current_user_from_cookie(request)
        user_id = current_user.get("sub")
        email = current_user.get("email")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found in token")
        
        return {
            "id": user_id,
            "email": email,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not authenticated")