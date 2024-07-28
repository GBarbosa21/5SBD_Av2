from fastapi import FastAPI
from .database import engine, Base
from .routes import router as main_router

# Inicialize o banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registre as rotas
app.include_router(main_router)
