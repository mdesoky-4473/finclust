from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy, BearerTransport
from app.routes import router
from app.models import User
from app.schemas import UserRead, UserCreate, UserUpdate
from app.user_manager import get_user_manager


SECRET = "supersecret1227"  # Use a secure env variable in production

cookie_transport = CookieTransport(cookie_max_age=3600)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()

# 🚨 Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://finclust-insights.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"]
)

@app.get("/")
def read_root():
    return {"message": "FinClust API is running"}
