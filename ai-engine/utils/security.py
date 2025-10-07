"""
Security utilities for AlgoMaster-Studio AI Engine
"""

import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, status
from passlib.context import CryptContext
from utils.logger import setup_logger

logger = setup_logger("security")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "algomaster-studio-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

async def verify_token(token: str) -> str:
    """
    Verify JWT token and return user ID
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Additional token validation (check expiration, etc.)
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.info(f"✅ Token verified for user: {user_id}")
        return user_id
        
    except jwt.PyJWTError as e:
        logger.warning(f"❌ Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_demo_token() -> str:
    """Create a demo token for testing purposes"""
    demo_data = {
        "sub": "demo_user_12345",
        "username": "demo@algomaster.studio",
        "role": "demo",
        "features": ["ai_analysis", "visualizations", "benchmarking"]
    }
    
    return create_access_token(demo_data, expires_delta=timedelta(hours=24))

def validate_api_key(api_key: str) -> bool:
    """Validate API key for external integrations"""
    # In production, this would check against a database of valid API keys
    valid_api_keys = [
        "algomaster_api_key_dev_123456",
        "algomaster_api_key_prod_789012"
    ]
    
    return api_key in valid_api_keys

def sanitize_code_input(code: str) -> str:
    """
    Sanitize code input to prevent malicious execution
    """
    # Remove potentially dangerous imports and statements
    dangerous_patterns = [
        "import os",
        "import sys", 
        "import subprocess",
        "exec(",
        "eval(",
        "open(",
        "file(",
        "__import__",
        "globals()",
        "locals()",
        "vars()",
        "dir()",
        "getattr",
        "setattr",
        "delattr",
        "hasattr"
    ]
    
    sanitized_code = code
    
    for pattern in dangerous_patterns:
        if pattern in sanitized_code.lower():
            logger.warning(f"⚠️ Potentially dangerous pattern detected and removed: {pattern}")
            sanitized_code = sanitized_code.replace(pattern, f"# REMOVED: {pattern}")
    
    return sanitized_code

def rate_limit_check(user_id: str, endpoint: str) -> bool:
    """
    Check rate limiting for user requests
    In production, this would use Redis or similar
    """
    # Simplified rate limiting (in production, use Redis with sliding window)
    # For demo, we'll allow all requests
    return True

class SecurityMiddleware:
    """Security middleware for additional protection"""
    
    @staticmethod
    def validate_request_size(content_length: int, max_size: int = 1024 * 1024) -> bool:
        """Validate request content size"""
        return content_length <= max_size
    
    @staticmethod
    def sanitize_headers(headers: Dict[str, str]) -> Dict[str, str]:
        """Sanitize request headers"""
        safe_headers = {}
        
        allowed_headers = [
            "authorization", "content-type", "accept",
            "user-agent", "origin", "referer"
        ]
        
        for key, value in headers.items():
            if key.lower() in allowed_headers:
                safe_headers[key] = value[:1000]  # Limit header length
        
        return safe_headers
    
    @staticmethod
    def detect_suspicious_patterns(content: str) -> List[str]:
        """Detect suspicious patterns in content"""
        suspicious_patterns = [
            r"<script.*?>.*?</script>",  # XSS
            r"javascript:",              # JavaScript protocol
            r"on\w+\s*=",               # Event handlers
            r"eval\s*\(",               # eval function
            r"exec\s*\(",               # exec function
            r"__.*__",                  # Python special methods
        ]
        
        detected = []
        import re
        
        for pattern in suspicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                detected.append(pattern)
        
        return detected

def create_secure_environment() -> Dict[str, Any]:
    """Create a secure execution environment for code analysis"""
    return {
        "restricted_builtins": {
            # Safe built-in functions only
            "len": len,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "min": min,
            "max": max,
            "sum": sum,
            "abs": abs,
            "sorted": sorted,
            "reversed": reversed,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
        },
        "allowed_modules": [
            "math",
            "random",
            "collections",
            "itertools",
            "functools"
        ],
        "max_execution_time": 5.0,  # seconds
        "max_memory_usage": 100,    # MB
        "max_output_size": 10000    # characters
    }

# Authentication decorators and helpers
def require_authentication(func):
    """Decorator to require authentication for endpoints"""
    async def wrapper(*args, **kwargs):
        # This would be implemented as a FastAPI dependency
        return await func(*args, **kwargs)
    return wrapper

def require_api_key(func):
    """Decorator to require API key for external access"""
    async def wrapper(*args, **kwargs):
        # This would validate API key from headers
        return await func(*args, **kwargs)
    return wrapper

# Constants for security configuration
SECURITY_CONFIG = {
    "max_code_length": 50000,      # Maximum code input length
    "max_requests_per_minute": 60,  # Rate limiting
    "max_requests_per_hour": 1000,  # Rate limiting
    "session_timeout": 3600,        # Session timeout in seconds
    "max_concurrent_executions": 5, # Max concurrent code executions per user
    "allowed_file_extensions": [".py", ".cpp", ".java", ".js"],
    "blocked_ip_patterns": [],      # IP patterns to block
    "security_headers": {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
    }
}

logger.info("🔒 Security utilities initialized with comprehensive protection")