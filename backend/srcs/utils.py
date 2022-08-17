from datetime import datetime
from datetime import timedelta

def chunk_list(m: list[list], x: int) -> list[list]:
    return [m[i:i+x] for i in range(0, len(m), x)]

def get_nova_range(white_nova_start: datetime) -> dict:
	actual_date = datetime.utcnow() 
	end = white_nova_start+ timedelta(days=14)
	while (actual_date.timestamp() >= end.timestamp()):
		white_nova_start = white_nova_start + timedelta(days=14)
		end = end + timedelta(days=14)
	return {"start": white_nova_start, "end": end}
