from fastapi import HTTPException, status

token_validation_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate token",
    )

credentials_validation_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Credentials is not valid",
    )
