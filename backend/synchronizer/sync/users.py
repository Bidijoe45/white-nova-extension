from datetime import datetime

from sqlalchemy.orm import Session

from intra import ic
from models import User

def sync_users(session: Session, from_date: datetime, cursus_id: int, campus_id: int) -> None:
	if from_date is None:
		from_date = datetime(1970, 1, 1)
	params: dict = {
		"filter[user_id]": 65996, #remove before prod
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
