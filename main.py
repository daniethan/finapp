from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.dbconfig import Base, engine
import uvicorn
from src.routers import expense_routers, income_routers, user_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> _AsyncGeneratorContextManager[None]:
    # Create the tables in the database
    # on app start up.
    Base.metadata.create_all(engine)
    yield
    # clean up code after shutdown goes here


app = FastAPI(lifespan=lifespan)


@app.get("/", tags=["Root"])
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


app.include_router(router=user_router.router)

# Expense Records routes
app.include_router(router=expense_routers.router)

# Income Records routes
app.include_router(router=income_routers.router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
