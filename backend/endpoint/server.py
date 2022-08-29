from datetime import timedelta, datetime

from flask import Flask, Response, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session
from sqlalchemy import select

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
			query = select(Location).where(Location.user_id == user_id, Location.created_at >= white_nova_range["start"])
			locations = session.execute(query).scalars().all()
			total_seconds = 0
			for location in locations:
				location_start = location.begin_at
				location_end = datetime.now() 
				if location.end_at is not None:
					location_end = location.end_at
				total_seconds += (location_end.timestamp() - location_start.timestamp())
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

	def index(self, login: str) -> Response:
		with Session(self.engine) as session:
			query = select(User.id).where(User.login == login)
			result = session.execute(query).fetchone()
			
			if result is None:
				return jsonify({
					"error": True,
					"message": "Login not valid"
				})
			
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
