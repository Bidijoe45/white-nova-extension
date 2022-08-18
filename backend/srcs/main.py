from os.path import exists
from time import sleep
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from intra import ic
from models import Base, User, Event, Feedback
from sync.locations import sync_locations
from utils import chunk_list, get_current_nova_start

def sync_events(session: Session, last_update: datetime, campus_id: int, cursus_id: int) -> None:
	if last_update is None:
		last_update = datetime(2022, 6, 1)
	params = {
				"range[updated_at]": f"{last_update},{datetime.utcnow()}"
			}
	events = ic.pages_threaded(f"campus/{campus_id}/cursus/{cursus_id}/events", params=params)
	events_objs = []
	current_events: list[int] = session.execute(select(Event.id).where(Event.end_at >= last_update)).scalars().all()
	for event in events:
		if event["id"] in current_events and "Evento Whitenover" not in event["description"]:
			session.execute(delete(Event).where(Event.id == event["id"]))
			continue
		if "Evento Whitenover" not in event["description"]:
			continue
		events_objs.append(Event(
				id = event["id"],
				end_at = datetime.strptime(event["end_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
				))
	session.add_all(events_objs)

def	sync_feedbacks(session: Session, last_update: datetime, nova_range: dict) -> None:
	if last_update is None:
		last_update = nova_range["start"]
	searched_users_ids_query = select(User.id).where(User.last_search >= (datetime.utcnow() - last_update))
	searched_users_ids = session.execute(searched_users_ids_query)
	user_id_chunks = chunk_list(searched_users_ids.scalars().all(), 100)
	feedbacks: list = []
	for n in user_id_chunks:
		params = {
			"filter[user_id]": ",".join(map(str, n)),
			"filter[feedbackable_type]": "Event",
			"range[created_at]": f"{last_update},{datetime.utcnow()}"
		}
		feedback_page: list = ic.pages_threaded("feedbacks", params=params)
		feedbacks.append(feedback_page)
	total_feedbacks = [item for sublist in feedbacks for item in sublist]
	feedbacks_objs = []
	whitenover_events = session.execute(select(Event.id)).scalars().all()
	for feedback in total_feedbacks:
		if feedback["feedbackable_id"] not in whitenover_events:
			continue
		feedbacks_objs.append(Feedback(
				id = feedback["id"],
				created_at = datetime.strptime(feedback["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
				user_id = feedback["user"]["id"],
				event_id = feedback["feedbackable_id"],
			))
	session.add_all(feedbacks_objs)

@compiles(Insert)
def insert_skip_unique(insert, compiler, **kw):
	return compiler.visit_insert(insert.prefix_with("OR IGNORE"), **kw)

def init_db() -> Engine:
	engine = create_engine("sqlite:///db.sqlite", future=True)
	Base.metadata.create_all(engine)
	return engine

if __name__ == "__main__":
	cursus_id: int = 21
	campus_id: int = 22
	event_string: str = "Evento Whitenover"
	white_nova_start = get_current_nova_start(datetime(2022, 7, 15, 10))
	engine: Engine = init_db()
	last_run: datetime = None

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
				# sync_users(session, last_run, cursus_id, campus_id)
				sync_locations(session, last_run, white_nova_start)
				# sync_scale_teams(session, last_run, get_nova_range(white_nova_start))
				# sync_events(session, last_run, campus_id, cursus_id)
				# sync_feedbacks(session, last_run, get_nova_range(white_nova_start))
				session.commit()
			print(f"[siva:backend/sync] Operation finished correctly at '{datetime.utcnow()}'")
			last_run = sync_start
		except Exception as e:
			print(f"[siva:backend/sync] Operation failed at '{datetime.utcnow()}' with error: '{e}'")
			last_run = None
			sleep(1)
			continue
		sleep(5) # 86400s -> 1d
