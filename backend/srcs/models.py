from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    login = Column(String(16), unique=True)
    last_search = Column(DateTime, default=datetime.now(), index=True) # TODO cambiar default a None por eficiencia

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

class EventUser(Base):
    __tablename__ = "events_users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, nullable=False)
    event_name = Column(String(128), nullable=False)
    event_description = Column(String(2048), nullable=False)
    begin_at = Column(DateTime, index=True, nullable=False)
    end_at = Column(DateTime)

    user = relationship("User")

    def __repr__(self) -> str:
        return f"EventUser<id: {self.id}, user_id: {self.user_id}, \
                event_id: {self.event_id}, event_name: {self.event_name}, \
                event_description: {self.event_description}, \
                begin_at: {self.begin_at}, end_at: {self.end_at}>"