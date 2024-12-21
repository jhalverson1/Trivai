from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from routes.game import router as game_router
import json
import os

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://frontend:3000",
    "https://*.railway.app",
    "*",  # Remove in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the game routes
app.include_router(game_router, prefix="/api")

# Check answer endpoint
@app.post("/api/check-answer")
async def check_answer(answer_data: dict):
    user_answer = answer_data.get('answer', '').upper()
    correct_answer = answer_data.get('correct_answer', '')
    
    if ')' in correct_answer:
        correct_answer = correct_answer.split(')')[0].strip()
    
    is_correct = user_answer == correct_answer.upper()
    return {
        "correct": is_correct,
        "correct_answer": correct_answer
    }

# Mount static files before the 404 handler
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Handle 404 errors
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Route {request.url.path} not found"}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True) 