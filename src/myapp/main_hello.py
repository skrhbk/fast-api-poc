from fastapi import FastAPI

from src.myapp.routers import wafers

# app = FastAPI(dependencies=[Depends(get_tsmc_uid)])
app = FastAPI()
app.include_router(wafers.router)


@app.get("/")
async def root():
    return {"message": "Hello My Router App!"}