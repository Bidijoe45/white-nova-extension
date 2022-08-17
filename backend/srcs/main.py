from os.path import exists
from time import sleep
from datetime import datetime


from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import update

from utils import chunk_list, get_nova_range
from intra import ic
from models import Base, User, Location

def sync_users(session: Session, from_date: datetime, cursus_id: int, campus_id: int) -> None:
	"""
	sync_users
	Using `from_date` as last sync date, takes all new cursuses and pushes all
	users into the database instance.
	If no `from_date` is provided (None), all users will be inserted.
	"""
	if from_date is None:
		from_date = datetime(1970, 1, 1)
	params = {
			"filter[campus_id]": campus_id,
			"flter[blackhole]": False,
			"range[created_at]": f"{from_date},{datetime.utcnow()}"
			}
	cursus_users = ic.pages_threaded(f"cursus/{cursus_id}/cursus_users", params=params)
	users = []
	for cursus_user in cursus_users:
		if "3b3-" in cursus_user["user"]["login"]:
			continue
		users.append(User(
				id = cursus_user["user"]["id"],
				login = cursus_user["user"]["login"]
				))
	session.add_all(users)

def sync_locations(session: Session, from_date: datetime, nova_range: dict) -> None:
	"""
	sync_locations
	Using `from_date` and `nova_range`, synchronises with the database them.
	If a location already existed, the end_at date is updated.
	"""
	if from_date is None:
		from_date = nova_range["start"]
	searched_users_ids_query = select(User.id).where(User.last_search >= (datetime.utcnow() - from_date))
	searched_users_ids = session.execute(searched_users_ids_query)
	user_id_chunks = chunk_list(searched_users_ids.scalars().all(), 100)
	locations = []
	locations_ended = [] # TODO check if these two lines are needed
	locations_active = []
	for n in user_id_chunks:
		params = {
			"filter[user_id]": ",".join(map(str, n))
		}
		locations_ended = ic.pages_threaded("locations", params={**params, **{"range[end_at]": f"{from_date},{datetime.utcnow()}"}})
		locations_active = ic.pages_threaded("locations", params={**params, **{"filter[active]": "true"}})
		locations.append(locations_ended)
		locations.append(locations_active)
	locations = [item for sublist in locations for item in sublist]
	locations_objs = []
	active_locations = session.execute(select(Location.id).where(Location.end_at == None)).scalars().all()
	for location in locations:
		if location["id"] not in active_locations:
			locations_objs.append(Location(
				id = location["id"],
				user_id = location["user"]["id"],
				begin_at = datetime.strptime(location["begin_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
				end_at = None if location["end_at"] is None else datetime.strptime(location["end_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
				host = location["host"]
			))
		elif location["end_at"] is not None:
			session.execute(update(Location).values({"end_at": datetime.strptime(location["end_at"], "%Y-%m-%dT%H:%M:%S.%fZ")}).where(Location.id == location["id"]))
	session.add_all(locations_objs)

def sync_events_users(session: Session, from_date: datetime, nova_range: dict, campus_id: int, filter_string: str) -> None:
	if from_date is None:
		from_date = nova_range["start"]

	params = {
		"range[end_at]": f"{from_date},{datetime.utcnow()}",
	}
	events = ic.pages_threaded(f"campus/{campus_id}/events", params=params)
	event_ids = list(map(lambda event: event["id"] if filter_string in event["description"] else None, events))
	event_ids = list(filter(lambda event_id: event_id is not None, event_ids))

	print(event_ids)

	#searched_users_ids_query = select(User.id).where(User.last_search >= (datetime.utcnow() - from_date))
	#searched_users_ids = session.execute(searched_users_ids_query)
	#user_id_chunks = chunk_list(searched_users_ids.scalars().all(), 100)
	#feedbacks = []
	#for n in user_id_chunks:
	#	params = {
	#		"filter[user_id]": ",".join(map(str, n)),
	#		"filter[feedbackable_type]": "Event",
	#		"range[created_at]": 
	#	}


@compiles(Insert)
def insert_skip_unique(insert, compiler, **kw):
	return compiler.visit_insert(insert.prefix_with("OR IGNORE"), **kw)

def init_db() -> Engine:
	engine = create_engine("sqlite:///db.sqlite", future=True)
	Base.metadata.create_all(engine)
	return engine

if __name__ == "__main__":
	engine: Engine = init_db()
	last_run: datetime = None
	white_nova_start = datetime(2022, 7, 15, 10)
	cursus_id: int = 21
	campus_id: int = 22
	event_string: str = "Evento Whitenover"

	# session: Session = Session(engine)
	# sync_locations(session, last_run, get_nova_range(white_nova_start))
	# session.commit()
	# session.close()	

	while True:
		if not exists("./db.sqlite"):
			engine = init_db()
			last_run = None
		try:
			print(f"[siva:backend/sync] Operation started at '{datetime.utcnow()}'")
			sync_start: datetime = datetime.utcnow()
			with Session(engine) as session:
				session: Session = Session(engine)
				session.execute("PRAGMA foreign_keys = ON;")
				#sync_users(session, last_run, cursus_id, campus_id)
				#sync_locations(session, last_run, get_nova_range(white_nova_start))
				sync_events_users(session, last_run, get_nova_range(white_nova_start), campus_id, event_string)
				session.commit()
			print(f"[siva:backend/sync] Operation finished correctly at '{datetime.utcnow()}'")
			last_run = sync_start
		except Exception as e:
			print(f"[siva:backend/sync] Operation failed at '{datetime.utcnow()}' with error: '{e}'")
			last_run = None
			sleep(1)
			continue
		sleep(5) # 86400s -> 1d
