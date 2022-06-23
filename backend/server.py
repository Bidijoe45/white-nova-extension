import json
import pendulum
from flask import Flask, jsonify, request
from lib_42api.intra import ic

ic.progress_bar=True

app = Flask(__name__)

def get_nova_range():
    white_nova_start = pendulum.datetime(2022, 6, 13);
    actual_date = pendulum.now();   

    end = white_nova_start.add(days=14);

    while (actual_date.timestamp() >= end.timestamp()):
        white_nova_start = white_nova_start.add(days=14);
        end = end.add(days=14);

    return {"start": white_nova_start, "end": end}

def get_time_between_dates(user_login, start_date, end_date) -> dict:
    params = {
        "range[begin_at]":f"{start_date.to_date_string()},{end_date.to_date_string()}",
    }
   
    locations = ic.pages_threaded(f"/users/{user_login}/locations", params=params)

    total = 0 

    for location in locations:

      location_begin_at = pendulum.parse(location['begin_at'])

      location_end_at = pendulum.now()

      if (location['end_at'] is not None):
        location_end_at = pendulum.parse(location['end_at'])

      total = total + (location_end_at.timestamp() - location_begin_at.timestamp())
    
    raw_hours = total / 60 / 60
    hours = int(total / 60 / 60)
    minutes = int((raw_hours - hours) * 60) 

    return {"hours": hours, "minutes": minutes, "raw_hours": raw_hours}

@app.route('/', methods=["GET"])
def index(): 
    options = request.args.to_dict()
    user_login = options.get('login') 

    date_range = get_nova_range();

    try:
        time = get_time_between_dates(user_login, date_range['start'], date_range['end'])
    except:
        return jsonify({"ok": 0, "message": "Error"})
    
    payload = {
        "hours": time['hours'],
        "minutes": time['minutes'],
        "raw_hours": time['raw_hours'],
        "start": date_range['start'].format("DD/MM/YYYY"),
        "end": date_range['end'].format("DD/MM/YYYY")
    }
    
    response = jsonify(payload)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

app.run()
