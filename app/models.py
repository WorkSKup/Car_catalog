from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime, Enum, Table, Column, Numeric, Integer
from datetime import datetime
from app import login, db


user_car = Table(
    "user_car",
    db.metadata,
    Column("user.id", ForeignKey("users.id"), primary_key=True),
    Column("car.id", ForeignKey("cars.id"), primary_key=True)
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(32), nullable=False)
    photo: Mapped[str] = mapped_column(String(140), nullable=True)


    Car: Mapped[list["Car"]] = relationship(
        "Car",
        secondary=user_car,
        back_populates="users"
    )


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)



class Car(db.Model):
    __tablename__ = 'cars'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    manufacture_year: Mapped[int] = mapped_column(Integer, nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    image: Mapped[str] = mapped_column(String(140), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)


    users: Mapped[list["User"]] = relationship(
        "User",
        secondary=user_car,
        back_populates="Car"
    )