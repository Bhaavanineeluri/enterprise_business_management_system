from fastapi import FastAPI


app = FastAPI(
    title="Enterprise Business Management System",
    version="1.0.0",
    description="Enterprise Business Management System API",
)


@app.get("/")
def root():
    return {
        "message": "Enterprise Business Management System API",
        "version": "1.0.0",
    }
