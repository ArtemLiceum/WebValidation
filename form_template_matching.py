from fastapi import FastAPI
from pymongo import MongoClient
from app.routes import form_routes

# Initialize FastAPI and database
app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client.form_templates

# Set database client for routes
form_routes.db_client = client

# Include routes
app.include_router(form_routes.router, prefix="/forms")

if __name__ == "__main__":
    import uvicorn
    print("Starting application...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
