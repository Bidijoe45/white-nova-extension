from flask import Flask, Response, jsonify, request
from utils import get_current_nova_start
from datetime import timedelta, datetime

import sqlite3

class Server:
	def __init__(self) -> None:
		self.app = Flask(__name__)
		self.white_nova_start = get_current_nova_start(datetime(2022, 7, 15, 10))
		self.connection = sqlite3.connect('./db.sqlite', check_same_thread=False)
		self.define_routes()
		pass
	
	def define_routes(self) -> None:
		self.app.add_url_rule("/<login>", view_func=self.index)

	def get_next_cycle(self) -> int:
		nova_start: datetime = get_current_nova_start(self.white_nova_start)
		nova_end: datetime = nova_start + timedelta(days=14)
		next_cycle: int = nova_end - datetime.utcnow()
		return next_cycle.days
		

	def get_time(self, cursor: sqlite3.Cursor, user_id: int) -> dict:
		row: tuple = cursor.execute("""
		SELECT
			SUM((JULIANDAY(
				CASE WHEN end_at IS NULL
				THEN DATETIME('now')
				ELSE end_at
				END
			) - JULIANDAY(begin_at)) * 86400) AS hours
		FROM locations
		WHERE user_id=(?)
		""", (user_id, )).fetchone()

		if row is None:
			return {
					"hours": 0,
					"minutes": 0
				}

		raw_hours: float = row[0] / 60 / 60
		hours: int = int(raw_hours)

		return {
				"hours": hours,
				"minutes": int((raw_hours - hours) * 60) 
			}

	def get_evaluations(self, cursor: sqlite3.Cursor, user_id: int) -> dict:
		row: tuple = cursor.execute("SELECT COUNT(id) FROM scale_teams WHERE user_id=(?)", (user_id, )).fetchone()

		if row is None:
			return 0
		return row[0]

	def get_events():
		pass

	def index(self, login: str) -> Response:
		cursor: sqlite3.Cursor = self.connection.cursor()
		row: tuple = cursor.execute(f"SELECT id FROM users WHERE login=(?)", (login, )).fetchone()

		if row is None:
			return jsonify({
				"error": True,
				"message": "Login not valid"
			})
		
		time: dict = self.get_time(cursor, row[0])

		payload: dict = {
				"hours": time["hours"],
				"minutes": time["minutes"],
				"evaluations": self.get_evaluations(cursor, row[0]),
				"events": "",
				"next_cycle": self.get_next_cycle()
		}

		cursor.close()
		return jsonify(payload)

if __name__ == "__main__":
	server: Server = Server()
	server.app.run(host="0.0.0.0", port=8080)
