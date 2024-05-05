# Normal comment
# * yellow comment
# ? blue comment
# ! red comment
# // Strike though comment
from mongoengine import connect
from passlib.context import CryptContext

from config import Config
from src.planner.models.user import User

connect(
    host=Config.MONGO_HOST,
    db=Config.MONGO_DB,
    username=Config.MONGO_USER,
    password=Config.MONGO_PASSWORD,
)


# User.create({"email": "adamhenderson90@gmail.com", "password": "password", "username": "Adam"})
context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = context.hash("password")

User.objects(email="adamhenderson90@gmail.com").update_one(password=password_hash)
