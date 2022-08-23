from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import backref, declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    login = Column(String(16), unique=True)
    last_search = Column(DateTime, default=(datetime.utcnow() - timedelta(days=1)), index=True)

    def __repr__(self) -> str:
        return f"User<id: {self.id}, login: {self.login}, last_search: {self.last_search}>"

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    begin_at = Column(DateTime, index=True, nullable=False)
    end_at = Column(DateTime)
    host = Column(String(6))

    user = relationship("User")

    def __repr__(self) -> str:
        return f"Location<id: {self.id}, user_id: {self.user_id}, \
                begin_at: {self.begin_at}, end_at: {self.end_at}, host: {self.host}>"

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    end_at = Column(DateTime, index=True)

    def __repr__(self) -> str:
        return f"Event<id: {self.id}, end_at: {self.end_at} >"

class ScaleTeam(Base):
    __tablename__ = "scale_teams"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filled_at = Column(DateTime, index=True, nullable=True)

    user = relationship("User")

    def __repr__(self) -> str:
        return f"ScaleTeam<id: {self.id}, user_id: {self.user_id}, \
                filled_at: {self.filled_at}>"

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    created_at = Column(DateTime, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    user = relationship("User")
    event = relationship("Event", backref=backref("feedbacks", cascade="all,delete,delete-orphan"))

    def __repr__(self) -> str:
        return f"Feedback<id: {self.id}, created_at: {self.created_at}, user_id: {self.user_id}, \
                event_id: {self.event_id}>"
