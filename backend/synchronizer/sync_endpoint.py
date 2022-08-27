from datetime import datetime

from flask import Flask
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from utils import get_current_nova_start
from sync.feedbacks import sync_feedbacks
from sync.locations import sync_locations
from sync.scale_teams import sync_scale_teams

class SyncEndpoint:
    def __init__(self, engine: Engine, campus_id: int, cursus_id: int, white_nova_start: datetime):
        self.engine = engine 
        self.campus_id = campus_id
        self.cursus_id = cursus_id
        self.white_nova_start = white_nova_start
        self.app = Flask(__name__)

    def sync_user_data(self, id):
        print(id)
        with Session(self.engine) as session:
            session.execute("PRAGMA foreign_keys = ON;")
            white_nova_start: datetime = get_current_nova_start(self.white_nova_start)
            sync_feedbacks(session, white_nova_start, [id])
            session.commit()
            sync_locations(session, white_nova_start, [id])
            session.commit()
            sync_scale_teams(session, white_nova_start, [id])
            session.commit()
        return "OK", 200;
    
    def run(self):
        self.app.add_url_rule("/sync/<int:id>", view_func=self.sync_user_data)
        self.app.run(host="localhost", port=8081)
