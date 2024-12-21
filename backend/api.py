from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from routes import game

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.railway.app",
        "http://backend:8000",
        "http://frontend:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the game routes first
app.include_router(game.router, prefix="/api")

# Root route handler
@app.get("/")
async def root():
    return JSONResponse(content={"status": "ok", "message": "API is running"})

# Handle 404 errors
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Route {request.url.path} not found"}
    )

# Mount static files last
app.mount("/", StaticFiles(directory="static", html=True))