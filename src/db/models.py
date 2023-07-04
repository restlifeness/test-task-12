
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    """
    Base model for all tables
    
    Attributes:
        id (int): Primary key for all tables
        created_at (datetime): Date and time of creation
        updated_at (datetime): Date and time of last update
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class User(BaseModel):
    __tablename__ = "users"
    """
    User model

    Attributes:
        username (str): Username of user
        hashed_password (str): Password of user
        email (str): Email of user
        first_name (str): First name of user
        last_name (str): Last name of user
        is_active (bool): Whether user is active or not
    """

    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)

    email = Column(String(254), unique=True, nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)

    is_active = Column(Boolean, default=True)


class Post(BaseModel):
    __tablename__ = "posts"
    """
    Post model

    Attributes:
        title (str): Title of post
        content (str): Content of post
        likes (int): Number of likes on post
        author_id (int): ID of user who created post
    """

    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)

    topic = Column(String(50), nullable=True)

    likes = Column(Integer, default=0)

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", backref="posts")
