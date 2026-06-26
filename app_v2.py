from fastapi import FastAPI, Request, HTTPException
import redis
import os

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request path: {request.url.path}")
    response = await call_next(request)
    return response

@app.get("/")
def root():
    return {"message": "FastAPI v2 canary is working"}

@app.post("/cache")
def store_value(key: str, value: str):
    try:
        redis_client.set(key, value)
    except redis.exceptions.RedisError as error:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(error)}")

    return {"message": f"Stored key '{key}'"}

@app.get("/cache")
def get_value(key: str):
    try:
        value = redis_client.get(key)
    except redis.exceptions.RedisError as error:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(error)}")

    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")

    return {"key": key, "value": value.decode()}