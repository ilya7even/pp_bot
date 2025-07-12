from sqlalchemy import create_engine, Column, Integer, String, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    pp_length = Column(Float, default=0.0)
    last_updated = Column(String, default="1970-01-01")

Base.metadata.create_all(engine)

def update_pp(user_id, username):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()

    now = datetime.utcnow().date().isoformat()
    if user:
        if user.last_updated == now:
            session.close()
            return None, user.pp_length  # уже сегодня обновлял

        change = round(random.uniform(-5, 10), 2)
        user.pp_length = max(0, user.pp_length + change)
        user.last_updated = now
    else:
        change = round(random.uniform(1, 10), 2)
        user = User(id=user_id, username=username, pp_length=change, last_updated=now)
        session.add(user)

    session.commit()
    length = user.pp_length
    session.close()
    return change, length

def get_user_pp(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    return user.pp_length if user else None

def get_top_users(limit=10):
    session = Session()
    users = session.query(User).order_by(User.pp_length.desc()).limit(limit).all()
    session.close()
    return [(u.username, u.pp_length) for u in users]
