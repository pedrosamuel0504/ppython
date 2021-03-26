from sqlalchemy import Column,Integer , String , Boolean ,ForeignKey,create_engine
from sqlalchemy.orm import relationship
from dbs import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner",cascade="all, delete, delete-orphan")

    def __repr_(self):
        return f" ID:{self.id} ---- User email: {self.email} ---- Is Active:{self.is_active}"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
