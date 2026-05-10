from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import timedelta
from app.schemas import (
    SignupRequest, LoginRequest, TokenResponse,
    RefreshTokenRequest, PasswordResetRequest, NewPasswordRequest, UserResponse
)
from app.core.security import (
    create_access_token, create_refresh_token, decode_token, get_current_user
)
from app.core.database import get_db, SupabaseDB
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=TokenResponse)
async def signup(
    request: SignupRequest,
    db: SupabaseDB = Depends(get_db)
):
    """
    Register a new user using Supabase Auth
    """
    # 1. Create user in Supabase Auth using admin API to bypass email confirmation
    try:
        auth_res = db.client.auth.admin.create_user({
            "email": request.email,
            "password": request.password,
            "email_confirm": True,
            "user_metadata": {"name": request.name, "role": request.role.value}
        })
        auth_user = auth_res.user
    except Exception as e:
        # Check if user already exists
        existing_user = db.query("users").select("*").eq("email", request.email).execute()
        if existing_user.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating auth user: {str(e)}"
        )
    
    # 2. Create user record in our public.users table
    user_data = {
        "id": auth_user.id,
        "email": request.email,
        "name": request.name,
        "role": request.role.value,
        "is_active": True
    }
    
    try:
        db.insert("users", user_data)
    except Exception as e:
        # Cleanup auth user if DB insert fails
        db.client.auth.admin.delete_user(auth_user.id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user profile: {str(e)}"
        )
    
    # 3. Create our custom tokens
    access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    access_token = create_access_token(
        data={"sub": auth_user.id, "email": request.email, "role": request.role.value},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": auth_user.id, "email": request.email}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: SupabaseDB = Depends(get_db)
):
    """
    Login with email and password using Supabase Auth
    """
    # 1. Verify with Supabase Auth
    try:
        # Note: We use the regular sign_in_with_password for validation
        auth_res = db.client.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        auth_user = auth_res.user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # 2. Get user profile from our DB
    result = db.query("users").select("*").eq("id", auth_user.id).execute()
    user = result.data[0] if result.data else None
    
    if not user:
        # Sync case: Auth user exists but no profile. Create it.
        user_data = {
            "id": auth_user.id,
            "email": auth_user.email,
            "name": auth_user.user_metadata.get("full_name", "User"),
            "role": auth_user.user_metadata.get("role", "student"),
            "is_active": True
        }
        db.insert("users", user_data)
        user = user_data

    # 3. Create our custom tokens
    access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user["id"], "email": user["email"]}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token
    """
    try:
        payload = decode_token(request.refresh_token)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    email = payload.get("email")
    role = payload.get("role")
    
    access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    access_token = create_access_token(
        data={"sub": user_id, "email": email, "role": role},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=request.refresh_token
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
    db: SupabaseDB = Depends(get_db)
):
    """
    Get current user profile
    """
    result = db.query("users").select("*").eq("id", current_user["user_id"]).execute()
    user = result.data[0] if result.data else None
    
    if not user:
        # Auto-sync: If Auth user exists but profile is missing, recreate it
        try:
            # Get user from Supabase Auth to get latest metadata
            auth_user = db.client.auth.admin.get_user_by_id(current_user["user_id"]).user
            user_data = {
                "id": auth_user.id,
                "email": auth_user.email,
                "name": auth_user.user_metadata.get("full_name", auth_user.user_metadata.get("name", "User")),
                "role": auth_user.user_metadata.get("role", "student"),
                "is_active": True
            }
            db.insert("users", user_data)
            user = user_data
        except Exception as e:
            print(f"Failed to auto-sync user profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found and could not be synchronized."
            )
    
    return UserResponse(**user)

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
