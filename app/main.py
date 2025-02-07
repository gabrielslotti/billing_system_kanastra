import uvicorn
from fastapi import FastAPI

from app.adapters.entrypoints.invoice import router as invoice_router
from app.configs.dependency_injection import Container


container = Container()
app = FastAPI()

app.include_router(invoice_router)
app.container = container

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
