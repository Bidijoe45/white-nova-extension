from datetime import datetime
from os.path import exists
from time import sleep
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from chron import Chron
from models import Base
from sync.users import sync_users
from sync.locations import sync_locations
from sync.events import sync_events
from sync.locations import sync_locations
from sync.scale_teams import sync_scale_teams
from sync.feedbacks import sync_feedbacks
from utils import get_current_nova_start
from sync_endpoint import SyncEndpoint 

@compiles(Insert)
def insert_skip_unique(insert, compiler, **kw):
	return compiler.visit_insert(insert.prefix_with("OR IGNORE"), **kw)

def init_db() -> Engine:
	engine = create_engine("sqlite:///../db.sqlite", future=True)
	Base.metadata.create_all(engine)
	return engine

def database_synchronizer(engine):
	chron = Chron(campus_id=22, cursus_id=21, default_last_run=get_current_nova_start(datetime(2022, 7, 15, 10)))
	chron.add_job(sync_users, days=1, primary_object=True)
	chron.add_job(sync_events, hours=8, primary_object=True)
	chron.add_job(sync_feedbacks, minutes=5)
	chron.add_job(sync_scale_teams, minutes=5)
	chron.add_job(sync_locations, minutes=1)

	while True:
		if not exists("../db.sqlite"):
			engine = init_db()
			chron.clear_run_history()
		try:
			with Session(engine) as session:
				session.execute("PRAGMA foreign_keys = ON;")
				elapsed_time: int = chron.execute(session)
		except Exception as e:
			print(f"[siva:backend/synchronizer] Operation failed at '{datetime.utcnow()}' with error: '{e}'")
		sleep(1)

	
if __name__ == "__main__":
	engine: Engine = init_db()
	sync_thread: Thread = Thread(target=database_synchronizer, args=(engine,), daemon=True) 
	sync_thread.start()
	sync_endpoint = SyncEndpoint(engine, 22, 21, datetime(2022, 7, 15, 10))
	sync_endpoint.run()
