from datetime import datetime

from sqlalchemy.orm import Session

from intra import ic
from models import ScaleTeam
from utils import get_last_search_chunks

def	sync_scale_teams(session: Session, last_update: datetime, nova_range: dict) -> None:
	if last_update is None:
		last_update = nova_range["start"]
	user_id_chunks = get_last_search_chunks(session, last_update)
	scale_teams_filled: list = []
	for n in user_id_chunks:
		params = {
			"filter[user_id]": ",".join(map(str, n)),
			"range[filled_at]": f"{last_update},{datetime.utcnow()}"
		}
		scale_teams: list = ic.pages_threaded("scale_teams", params=params)
		scale_teams_filled.append(scale_teams)
	scale_teams_filled = [item for sublist in scale_teams_filled for item in sublist]
	scale_team_objs = []
	for scale_team in scale_teams_filled:
		if scale_team["filled_at"] is None:
			continue
		scale_team_objs.append(ScaleTeam(
				id = scale_team["id"],
				user_id = scale_team["corrector"]["id"],
				filled_at = datetime.strptime(scale_team["filled_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
			))
	session.add_all(scale_team_objs)