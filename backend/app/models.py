from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, Column
from app.database import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)  # 👈 This line ensures Alembic recognizes the PK
