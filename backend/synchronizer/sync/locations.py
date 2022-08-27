from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.engine import Result

from intra import ic
from models import Location
from utils import get_last_search_chunks, strtodate

def __get_api_locations(user_id_chunks: list, last_update: datetime) -> list:
	locations: list[list] = []
	for n in user_id_chunks:
		params: dict = {
			"filter[user_id]": ",".join(map(str, n))
		}
		locations_ended: list[dict] = ic.pages_threaded("locations", params={
			**params,
			**{"range[end_at]": f"{last_update},{datetime.utcnow()}"}
		})
		locations_active: list[dict] = ic.pages_threaded("locations", params={
			**params,
			**{"filter[active]": "true"}
		})
		locations.append(locations_ended)
		locations.append(locations_active)
	return [item for sublist in locations for item in sublist]

def sync_locations(session: Session, last_update: datetime, users_ids: list) -> None:
	user_id_chunks: list[list] = []
	if users_ids is None:
		user_id_chunks: list[list] = get_last_search_chunks(session, last_update)
	else:
		user_id_chunks.append(users_ids)
	if not user_id_chunks:
		return
	locations: list[dict] = __get_api_locations(user_id_chunks, last_update)
	print(locations)
	active_locations: Result = session.execute(select(Location.id).where(Location.end_at == None)).scalars().all()
	locations_objs: list[Location] = []
	for location in locations:
		if location["id"] not in active_locations:
			locations_objs.append(Location(
				id = location["id"],
				user_id = location["user"]["id"],
				begin_at = strtodate(location["begin_at"]),
				end_at = strtodate(location["end_at"]),
				host = location["host"]
			))
		elif location["end_at"] is not None:
			session.execute(update(Location)
				.values({"end_at": strtodate(location["end_at"])})
				.where(Location.id == location["id"]))
	session.add_all(locations_objs)

