import uvicorn
from fastapi import FastAPI
from app.api.routers import routers

def main():
    app = FastAPI()
    for rout in routers:
        app.include_router(rout)
    uvicorn.run(app)

if __name__ == '__main__':
    main()
