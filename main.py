from fastapi import FastAPI, Request
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "Medical Diagnosis API is running 🚀"}

# Healthcheck endpoint
@app.get("/health")
def health_check():
    logger.info("Health check endpoint hit")
    return {"message": "ok"}

# Middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"➡️ {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"⬅️ {response.status_code} {request.method} {request.url}")
    return response

# Entry point for local debugging only
def main():
    print("Hello from medical diagnosis")

if __name__ == "__main__":
    main()
