"""Security utilities for authentication and input validation."""
import re
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Request, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import get_db

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production-use-environment-variable"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Rate limiting storage
rate_limit_storage = defaultdict(list)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get the current authenticated user."""
    from .models.user import User  # Import here to avoid circular imports
    
    username = verify_token(token)
    user = db.query(User).filter(User.email == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def validate_task_input(title: str, description: Optional[str] = None):
    """Validate task input for security."""
    if not title or len(title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    if len(title) > 200:
        raise HTTPException(status_code=400, detail="Title too long (max 200 characters)")
    
    if description and len(description) > 1000:
        raise HTTPException(status_code=400, detail="Description too long (max 1000 characters)")
    
    # Check for potential XSS patterns
    dangerous_patterns = [
        r'<script.*?>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe.*?>',
        r'<object.*?>',
        r'<embed.*?>'
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, title, re.IGNORECASE) or (description and re.search(pattern, description, re.IGNORECASE)):
            raise HTTPException(status_code=400, detail="Invalid characters detected in input")

def validate_priority_values(*values):
    """Validate priority values are within acceptable range."""
    for value in values:
        if value is not None and (value < 1 or value > 10):
            raise HTTPException(status_code=400, detail="Priority values must be between 1 and 10")

def rate_limit_middleware(request: Request, max_requests: int = 100, window_minutes: int = 1):
    """Simple rate limiting middleware."""
    client_ip = request.client.host
    now = time.time()
    window_start = now - (window_minutes * 60)
    
    # Clean old entries
    rate_limit_storage[client_ip] = [
        timestamp for timestamp in rate_limit_storage[client_ip] 
        if timestamp > window_start
    ]
    
    # Check rate limit
    if len(rate_limit_storage[client_ip]) >= max_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    # Add current request
    rate_limit_storage[client_ip].append(now)
