from datetime import datetime
from datetime import timedelta

from sqlalchemy.orm import Session
from sqlalchemy import select

from models import User

def chunk_list(m: list[list], x: int) -> list[list]:
    return [m[i:i+x] for i in range(0, len(m), x)]

def strtodate(string: str) -> datetime:
	if string is None:
		return None
	return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%fZ")

def get_last_search_chunks(session: Session, last_update: datetime):
	searched_users_ids_query = select(User.id).where(User.last_search >= (datetime.utcnow() - last_update))
	searched_users_ids = session.execute(searched_users_ids_query)
	return chunk_list(searched_users_ids.scalars().all(), 100)

def get_current_nova_start(white_nova_start: datetime) -> datetime:
	actual_date: datetime = datetime.utcnow() 
	end: datetime = white_nova_start+ timedelta(days=14)
	while (actual_date.timestamp() >= end.timestamp()):
		white_nova_start = white_nova_start + timedelta(days=14)
		end = end + timedelta(days=14)
	return white_nova_start
