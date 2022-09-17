from datetime import datetime
import json

from sqlalchemy.orm import Session

from intra import ic
from models import User

def sync_users(session: Session, from_date: datetime, cursus_id: int, campus_id: int) -> None:
	users_ignored_json_file = open("../users-ignored.json", "r")
	users_ignored_str = users_ignored_json_file.read()
	users_ignored_json_file.close()
	users_ignored = json.loads(users_ignored_str)["users_to_ignore"]
	if from_date is None:
		from_date = datetime(1970, 1, 1)
	params: dict = {
		"filter[campus_id]": campus_id,
		"flter[blackhole]": False,
		"range[created_at]": f"{from_date},{datetime.utcnow()}"
	}
	cursus_users = ic.pages_threaded(f"cursus/{cursus_id}/cursus_users", params=params)
	users = []
	for cursus_user in cursus_users:
		if "3b3-" in cursus_user["user"]["login"]:
			continue
		if cursus_user["user"]["login"] in users_ignored:
			print("user ignored")
			continue
		users.append(User(
				id = cursus_user["user"]["id"],
				login = cursus_user["user"]["login"]
				))
	session.add_all(users)
