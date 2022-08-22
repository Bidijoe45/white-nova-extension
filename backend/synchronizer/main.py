from os.path import exists
from time import sleep
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from models import Base
from sync.users import sync_users
from sync.locations import sync_locations
from sync.events import sync_events
from sync.locations import sync_locations
from sync.scale_teams import sync_scale_teams
from sync.feedbacks import sync_feedbacks
from utils import get_current_nova_start

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
				sync_users(session, last_run, cursus_id, campus_id)
				sync_events(session, last_run or white_nova_start, campus_id, cursus_id)
				sync_locations(session, last_run or white_nova_start)
				sync_scale_teams(session, last_run or white_nova_start)
				sync_feedbacks(session, last_run or white_nova_start)
				session.commit()
			print(f"[siva:backend/sync] Operation finished correctly at '{datetime.utcnow()}'")
			last_run = sync_start
		except Exception as e:
			print(f"[siva:backend/sync] Operation failed at '{datetime.utcnow()}' with error: '{e}'")
			last_run = None
			sleep(1)
			continue
		sleep(5) # 86400s -> 1d
