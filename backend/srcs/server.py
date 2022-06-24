import json
import pendulum
from flask import Flask, jsonify, request
from intra import ic

ic.progress_bar=True

app = Flask(__name__)


def get_nova_range(white_nova_start):
    actual_date = pendulum.now() 

    end = white_nova_start.add(days=14)

    while (actual_date.timestamp() >= end.timestamp()):
        white_nova_start = white_nova_start.add(days=14);
        end = end.add(days=14)

    return {"start": white_nova_start, "end": end}

def get_time_between_dates(user_login, start_date, end_date, white_nova_start) -> dict:
    params = {
            #"range[begin_at]":f"{start_date.to_date_string()},{end_date.to_date_string()}",
            "page[size]": 100
    }

    locations = ic.pages_threaded(f"/users/{user_login}/locations", params=params)

    total = 0 

    for location in locations:

        location_end_at = pendulum.now()

        if (location['end_at'] is not None):
            location_end_at = pendulum.parse(location['end_at'])
        
        if (location_end_at.timestamp() < white_nova_start.timestamp()): 
            continue

        location_begin_at = pendulum.parse(location['begin_at'])
        
        if (location_begin_at.timestamp() < white_nova_start.timestamp()):
            location_begin_at = white_nova_start

        total = total + (location_end_at.timestamp() - location_begin_at.timestamp())

    raw_hours = total / 60 / 60
    hours = int(total / 60 / 60)
    minutes = int((raw_hours - hours) * 60) 

    return {"hours": hours, "minutes": minutes, "raw_hours": raw_hours}

@app.route('/', methods=["GET"])
def index(): 
    white_nova_start = pendulum.datetime(2022, 6, 17)
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
            "events": events()
    }

    response = jsonify(payload)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def historic():
    white_nova_start = pendulum.datetime(2022, 6, 17)
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
    white_nova_start = pendulum.datetime(2022, 6, 17)
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
