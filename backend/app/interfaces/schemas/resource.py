from pydantic import BaseModel, Field


class AccessTokenRequest(BaseModel):
    """Access token request schema"""
    expire_minutes: int = Field(15, description="Token expiration time in minutes (max 15 minutes)", ge=1, le=15)


class SignedUrlResponse(BaseModel):
    """Signed URL response schema"""
    signed_url: str
    expires_in: int     # seconds
