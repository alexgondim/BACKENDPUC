from fastapi import FastAPI
from app.api.user_routes import user_router  # Importação absoluta baseada na estrutura de diretório
from app.database import init_db  # Importação absoluta
from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # O endereço do front-end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclua o roteador de usuários
app.include_router(user_router)

# Função de evento para inicializar o banco de dados quando a aplicação iniciar
@app.on_event("startup")
def startup_event():
    init_db()  # Chamada da função para inicializar o banco de dados



