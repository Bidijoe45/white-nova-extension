from datetime import datetime

from sqlalchemy.orm import Session

from intra import ic
from models import ScaleTeam
from utils import get_last_search_chunks, strtodate

def __get_scale_teams(user_id_chunks: list, last_update: datetime) -> dict:
	scale_teams: list[list] = []
	for n in user_id_chunks:
		params: dict = {
			"filter[user_id]": ",".join(map(str, n)),
			"range[filled_at]": f"{last_update},{datetime.utcnow()}"
		}
		scale_teams_page: list[dict] = ic.pages_threaded("scale_teams", params=params)
		scale_teams.append(scale_teams_page)
	return [item for sublist in scale_teams for item in sublist]

def	sync_scale_teams(session: Session, last_update: datetime, users_ids: list = None) -> None:
	user_id_chunks: list[list] = []
	if users_ids is None:
		user_id_chunks: list[list] = get_last_search_chunks(session, last_update)
	else:
		user_id_chunks.append(users_ids)
	if not user_id_chunks:
		return
	scale_teams: list[dict] = __get_scale_teams(user_id_chunks, last_update)
	scale_team_objs: list[ScaleTeam] = []
	for scale_team in scale_teams:
		if scale_team["filled_at"] is None:
			continue
		scale_team_objs.append(ScaleTeam(
				id = scale_team["id"],
				user_id = scale_team["corrector"]["id"],
				filled_at = strtodate(scale_team["filled_at"])
			))
	session.add_all(scale_team_objs)
