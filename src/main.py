import uvicorn

from fastapi import FastAPI

from routes import auth_router, user_router, posts_router

from core.settings import get_settings


settings = get_settings()
app = FastAPI(debug=settings.DEBUG)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(posts_router)


def main() -> None:
    uvicorn.run(
        'main:app',
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


if __name__ == '__main__':
    main()
