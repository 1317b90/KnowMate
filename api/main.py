from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import food,log,parsing,user
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# 设置静态目录images
app.mount("/images", StaticFiles(directory="images"), name="images")

app.include_router(food.app)
app.include_router(log.app)
app.include_router(parsing.app)
app.include_router(user.app)
