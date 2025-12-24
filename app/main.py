from fastapi import FastAPI
import uvicorn
from api import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to Contact Manager API"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

