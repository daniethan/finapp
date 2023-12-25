from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.dbconfig import Base, engine
import uvicorn
from src.routers import expense_routers, income_routers, user_router


app = FastAPI()


@app.on_event("startup")
def on_startup():
    # Create the tables in the database
    Base.metadata.create_all(engine)
    return None


@app.get("/", tags=["Root"])
async def root():
    return RedirectResponse(url="/docs")


app.include_router(router=user_router.router)

# Expense Records routes
app.include_router(router=expense_routers.router)

# Income Records routes
app.include_router(router=income_routers.router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
