# from sqlalchemy.orm import Session
# from ..data.crud import create_user, authenticate_user
# import jwt
# import datetime

# SECRET_KEY = "your_secret_key"

# def generate_token(email: str):
#     expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
#     token_data = {"sub": email, "exp": expiration}
#     return jwt.encode(token_data, SECRET_KEY, algorithm="HS256")

# def register_user(db: Session, email: str, password: str):
#     return create_user(db, email, password)

# def login_user(db: Session, email: str, password: str):
#     user = authenticate_user(db, email, password)
#     if not user:
#         return None
#     return generate_token(user.email)
