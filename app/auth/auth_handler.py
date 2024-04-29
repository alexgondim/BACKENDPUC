from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
 # substitua pelo caminho correto se necessário
from app.models.user_model import User as DBUser
from app.database import get_db



# definir o contexto de hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações para o seu JWT
# NOTA: Em um ambiente de produção, mantenha as chaves secretas de fato seguras!
SECRET_KEY = "um_secret_key_muito_seguro_que_deve_ser_mantido_em_segredo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthHandler:
    def get_password_hash(self, password):
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    def encode_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "sub": str(user_id),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload["sub"]
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
    def auth_wrapper(self, auth: str = Depends(oauth2_scheme)):
        return self.decode_token(auth)


# class AuthHandler:
#     def get_password_hash(self, password):
#         return pwd_context.hash(password)
    
#     def verify_password(self, plain_password, hashed_password):
#         return pwd_context.verify(plain_password, hashed_password)
    
#     def encode_token(self, user_id):
#         payload = {
#             "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
#             "sub": str(user_id),
#         }
#         return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

#     def decode_token(self, token):
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             return payload["sub"]
#         except JWTError:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
            
#     def auth_wrapper(self, auth: str = Depends(oauth2_scheme)):
#         return self.decode_token(auth)

# Esta função seria usada no lugar da lógica de autenticação que
# você implementaria em suas rotas/endpoints
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Implementação para verificar o usuário e senha na rota de login
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)