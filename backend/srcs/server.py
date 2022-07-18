import json
import pendulum
import datetime
from flask import Flask, jsonify, request
from intra import ic

ic.progress_bar=True

app = Flask(__name__)


def get_nova_range(white_nova_start):
    actual_date = pendulum.now() 

    end = white_nova_start.add(days=14)

    while (actual_date.timestamp() >= end.timestamp()):
        white_nova_start = white_nova_start.add(days=14)
        end = end.add(days=14)

    return {"start": white_nova_start, "end": end}

def get_time_between_dates(user_login, start_date, end_date, white_nova_start) -> dict:
    params = {
        "begin_at": f"{start_date}",
        "end_at": f"{end_date}"
    }

    locations = ic.get(f"/users/{user_login}/locations_stats", params=params)
    total = datetime.timedelta()
    for _, v in locations.json().items():
        (h, m, s) = v.split(':')
        total += datetime.timedelta(hours=int(h), minutes=int(m))
    raw_hours = total.total_seconds() / 60 / 60
    hours = int(total.total_seconds() / 60 / 60)
    minutes = int((raw_hours - hours) * 60)

    return {"hours": hours, "minutes": minutes, "raw_hours": raw_hours}

@app.route('/', methods=["GET"])
def index(): 
    white_nova_start = pendulum.from_format('2022-09-15 12', 'YYYY-MM-DD HH')
    options = request.args.to_dict()
    user_login = options.get('login') 
    date_range = get_nova_range(white_nova_start)

    try:
        time = get_time_between_dates(user_login, date_range['start'], date_range['end'], white_nova_start)
    except:
        return jsonify({"ok": 0, "message": "Error"})

    payload = {
            "hours": time['hours'],
            "minutes": time['minutes'],
            "raw_hours": time['raw_hours'],
            "start": date_range['start'].format("DD/MM/YYYY"),
            "end": date_range['end'].format("DD/MM/YYYY"),
            "evaluations": historic(),
            "events": events(),
            "next_cycle": int((date_range['end'].timestamp() - pendulum.now().timestamp()) / 60 / 60 / 24)
    }

    response = jsonify(payload)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def historic():
    white_nova_start = pendulum.from_format('2022-09-15 12', 'YYYY-MM-DD HH')
    options = request.args.to_dict()
    user_login = options.get('login') 

    date_range = get_nova_range(white_nova_start)

    params = {
        "sort": "-created_at",
        "filter[reason]": "Earning after defense",
        "range[created_at]": f"{date_range['start'].to_date_string()},{date_range['end'].to_date_string()}"
    }

    try:
        historic = ic.get(f"/users/{user_login}/correction_point_historics", params=params)
    except:
        return jsonify({"ok": 0})
    
    return len(historic.json())

def events():
    white_nova_start = pendulum.from_format('2022-09-15 12', 'YYYY-MM-DD HH')
    options = request.args.to_dict()
    user_login = options.get('login')
    date_range = get_nova_range(white_nova_start)

    params = {
        "sort": "-created_at",
        "range[created_at]": f"{date_range['start'].to_date_string()},{date_range['end'].to_date_string()}"
    }

    try:
        events = ic.get(f"/users/{user_login}/events_users", params=params)
    except:
        return jsonify({"ok": 0})
    return len(events.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
