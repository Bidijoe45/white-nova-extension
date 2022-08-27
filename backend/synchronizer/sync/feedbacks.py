from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from intra import ic
from models import Event, Feedback
from utils import get_last_search_chunks, get_current_nova_start

def __get_feedbacks(user_id_chunks: list, last_update: datetime) -> list:
	feedbacks: list = []
	for n in user_id_chunks:
		params: dict = {
			"filter[user_id]": ",".join(map(str, n)),
			"filter[feedbackable_type]": "Event",
			"range[created_at]": f"{last_update},{datetime.utcnow()}"
		}
		feedback_page: list[dict] = ic.pages_threaded("feedbacks", params=params)
		feedbacks.append(feedback_page)
	return [item for sublist in feedbacks for item in sublist]

def	sync_feedbacks(session: Session, last_update: datetime, users_ids: list = None) -> None:
	if last_update is None:
		last_update = get_current_nova_start()
	user_id_chunks: list[list] = []
	if users_ids is None:
		user_id_chunks: list[list] = get_last_search_chunks(session, last_update)
	else:
		user_id_chunks.append(users_ids)
	if not user_id_chunks:
		return
	feedbacks: list[dict] = __get_feedbacks(user_id_chunks, last_update)
	feedbacks_objs: list[Feedback] = []
	whitenover_events = session.execute(select(Event.id)).scalars().all()
	for feedback in feedbacks:
		if feedback["feedbackable_id"] not in whitenover_events:
			continue
		feedbacks_objs.append(Feedback(
			id = feedback["id"],
			created_at = datetime.strptime(feedback["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
			user_id = feedback["user"]["id"],
			event_id = feedback["feedbackable_id"],
		))
	session.add_all(feedbacks_objs)

