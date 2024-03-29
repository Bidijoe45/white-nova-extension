from datetime import timedelta, datetime
from threading import Thread

from flask import Flask, Response, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session
from sqlalchemy import select
import requests

from utils import get_current_nova_range
from models import Location, ScaleTeam, User, Feedback

class Server:
	def __init__(self) -> None:
		self.app = Flask(__name__)
		CORS(self.app)
		self.white_nova_start = datetime(2022, 7, 15, 10)
		self.engine = create_engine("sqlite:///../db.sqlite", future=True)
		self.define_routes()
	
	def define_routes(self) -> None:
		self.app.add_url_rule("/<login>", view_func=self.index)

	def get_next_cycle(self) -> int:
		nova_start: datetime = get_current_nova_range(self.white_nova_start)["start"]
		nova_end: datetime = nova_start + timedelta(days=14)
		next_cycle: int = nova_end - datetime.utcnow()
		return next_cycle.days

	def get_time(self, user_id: int) -> dict:
		with Session(self.engine) as session:
			white_nova_range = get_current_nova_range(self.white_nova_start)
			white_nova_start_offset = white_nova_range["start"] - timedelta(days=1)
			query = select(Location).where(Location.user_id == user_id, Location.begin_at >= white_nova_start_offset)
			locations = session.execute(query).scalars().all()
			total_seconds = 0
			last_location_end = None
			for location in locations:
				if location.end_at is not None and location.end_at < white_nova_range["start"]:
					continue
				location_start = location.begin_at
				location_end = datetime.utcnow() 
				if location.end_at is not None:
					location_end = location.end_at
				if location_start < white_nova_range["start"] and location_end > white_nova_range["start"]:
					location_start = white_nova_range["start"]
				if last_location_end is not None and last_location_end > location_start:
					location_start = last_location_end
				total_seconds += (location_end.timestamp() - location_start.timestamp())
				last_location_end = location_end
			hours = total_seconds / 60 / 60 
		return {
				"hours": hours,
				"minutes": (hours - int(hours)) * 60 
			}

	def get_evaluations(self, user_id: int) -> dict:
		with Session(self.engine) as session:
			white_nova_range = get_current_nova_range(self.white_nova_start)
			query = select(ScaleTeam).where(ScaleTeam.user_id == user_id, ScaleTeam.filled_at >= white_nova_range["start"])
			scale_teams = session.execute(query).scalars().all()

			return len(scale_teams)

	def get_events(self, user_id: int) -> int:
		with Session(self.engine) as session:
			white_nova_range = get_current_nova_range(self.white_nova_start)
			query = select(Feedback).where(Feedback.user_id == user_id, Feedback.created_at >= white_nova_range["start"])
			feedbacks = session.execute(query).scalars().all()

			if feedbacks is None:
				return 0

		return len(feedbacks)				

	def synchronizer_call(self, id):
		requests.get("http://localhost:8081/sync/" + str(id))
		pass

	def index(self, login: str) -> Response:
		with Session(self.engine) as session:
			query = select(User.id, User.last_search).where(User.login == login)
			result = session.execute(query).fetchone()
			
			if result is None:
				return jsonify({
					"error": True,
					"message": "Login not valid"
				})

			# if result.last_search < (datetime.utcnow() - timedelta(days=1)):
			# 	print("entra", result.id);
			# 	sync_call = Thread(target=self.synchronizer_call, args=(result.id,))
			# 	sync_call.start()
		
			user_id = result[0]
			session.execute(update(User).values({"last_search": datetime.utcnow()}).where(User.id == user_id))
			time: dict = self.get_time(user_id)

			payload: dict = {
					"raw_hours": time["hours"],
					"hours": int(time["hours"]),
					"minutes": int(time["minutes"]),
					"evaluations": self.get_evaluations(user_id),
					"events": self.get_events(user_id),
					"next_cycle": self.get_next_cycle()
			}
			session.commit()

		return jsonify(payload)

if __name__ == "__main__":
	server: Server = Server()
	server.app.run(host="0.0.0.0", port=8080)
