from fastapi import FastAPI

app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    return {"message": "Medical Diagnosis API is running 🚀"}

# Healthcheck endpoint
@app.get("/health")
def healthCheck():
    return {"message": "ok"}

def main():
    print("Hello from medicalreportdiagnosis!")

if __name__ == "__main__":
    main()
