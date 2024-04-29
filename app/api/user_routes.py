from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_model import User as DBUser
from app.schemas.user_schema import UserCreate, UserUpdate, User as SchemaUser
from app.services.via_cep_service import get_address_by_cep
from app.database import get_db
from app.auth.auth_handler import AuthHandler

user_router = APIRouter()
auth_handler = AuthHandler()

# @user_router.post("/users", response_model=SchemaUser)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     # Verificar se o usuário já existe
#     existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with this email already exists."
#         )
#     # Hash da senha e criação do usuário
#     hashed_password = auth_handler.get_password_hash(user.password)
#     db_user = DBUser(
#         email=user.email, 
#         hashed_password=hashed_password, 
#         full_name=user.full_name
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

@user_router.post("/users", response_model=SchemaUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se o usuário já existe
    existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
    # Hash da senha e criação do usuário
    hashed_password = auth_handler.get_password_hash(user.password)
    db_user = DBUser(
        email=user.email, 
        hashed_password=hashed_password, 
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user





@user_router.post("/token")
def login(user_credentials: UserCreate, db: Session = Depends(get_db)):
    user = auth_handler.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    token = auth_handler.encode_token(user.email)
    return {"token": token}

@user_router.get("/users/{user_id}", response_model=SchemaUser)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.put("/users/{user_id}", response_model=SchemaUser)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(DBUser).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    db.commit()
    return user

@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(DBUser).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}

@user_router.get("/cep/{cep}", response_model=SchemaUser)
def read_address(cep: str, db: Session = Depends(get_db)):
    address = get_address_by_cep(cep)
    if address:
        return address
    raise HTTPException(status_code=404, detail="CEP not found")