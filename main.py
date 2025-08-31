from fastapi import FastAPI

app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    return {"message": "Medical Diagnosis API is running 🚀"}

# Healthcheck endpoint
@app.get("/health")
def health_check():
    return {"message": "ok"}

# Entry point for local debugging only
def main():
    print("Hello from medical diagnosis")

if __name__ == "__main__":
    main()