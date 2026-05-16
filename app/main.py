from fastapi import FastAPI
from app.routers import supervisor
from app.db.database import init_db
from contextlib import asynccontextmanager


# Run DB init only once when the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
    yield

app = FastAPI(title="Hotel Multi-Agent Backend", lifespan=lifespan)


# Routers
# app.include_router(room_booking.router, prefix="/room-booking", tags=["Room"])
# app.include_router(food_ordering.router, prefix="/food-ordering", tags=["Food"])
app.include_router(supervisor.router, prefix="/chat", tags=["AI-Supervisor-Chat"])

# import uvicorn

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)

