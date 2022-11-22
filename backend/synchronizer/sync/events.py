from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from intra import ic
from models import Event

def sync_events(session: Session, last_update: datetime, cursus_id: int, campus_id: int) -> None:
	params: dict = {
		"range[updated_at]": f"{last_update},{datetime.utcnow()}"
	}
	events: list[dict] = ic.pages_threaded(f"campus/{campus_id}/cursus/{cursus_id}/events", params=params)
	events_objs: list[Event] = []
	current_events: list[int] = session.execute(select(Event.id).where(Event.end_at >= last_update)).scalars().all()
	for event in events:
		if event["id"] in current_events and "Evento Whitenover" not in event["description"].lower():
			session.execute(delete(Event).where(Event.id == event["id"]))
			continue
		if "Evento Whitenover" not in event["description"]:
			continue
		events_objs.append(Event(
				id = event["id"],
				end_at = datetime.strptime(event["end_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
			))
	session.add_all(events_objs)

