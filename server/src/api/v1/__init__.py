from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .actions import router as actions_router
from .supabase_auth import router as supabase_auth_router
from src.utils.supabase import supabase_config

app = FastAPI(title="TalentTrek API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register core routers
app.include_router(actions_router)

# Register only Supabase authentication router
app.include_router(supabase_auth_router)

# Serve static files
app.mount("/reports", StaticFiles(directory="data_output/reports"), name="reports") 