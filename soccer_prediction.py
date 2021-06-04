import json
import requests
from models import app, db
from datetime import datetime
from models import Predictions 
from flask import render_template
from random import randrange

@app.route("/call-predictions", methods=["POST", "GET"])
def get_prediction():
    today_date = datetime.now()
    formated_today_date = str(today_date)[:10]

    is_prediction_ready = Predictions.query.filter_by(date=formated_today_date).first()
    if is_prediction_ready:
        data = is_prediction_ready.prediction
        all_predictions = json.loads(data)["data"]
        
        all_odds = 1
        loss, won = (0, 0)
        list_of_bets = []

        for i in range(2):
            index = randrange(0, len(all_predictions))
            pred = all_predictions[index]
            list_of_bets.append(pred)
            all_predictions.remove(pred)

        for prediction in list_of_bets:
            if prediction["is_expired"]:
                predicted_type = prediction["prediction"]
                bet_status = prediction["status"]
                predicted_odds = prediction["odds"][predicted_type]
                print(predicted_type, predicted_odds, bet_status)
                all_odds *= int(predicted_odds)
                if bet_status == "won":
                    won += 1
                elif bet_status == "lost":
                    loss += 1
        
        print(loss, "loss", won, "won")
        print(all_odds)

        # print(f["data"][0], "PABABA")
        bets = processed_data(data)
        # print(bets)
        return render_template("prediction/predict.html", bets=bets)
    else:
        url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"

        querystring = {"iso_date": f"{formated_today_date}", "market":"classic", "federation":"UEFA"}

        headers = {
            'x-rapidapi-key': "7913f74345msh3ff0bc8b5d8a628p1aec75jsn32a9861c2524",
            'x-rapidapi-host': "football-prediction-api.p.rapidapi.com"
            }


        prediction_data = requests.request("GET", url, headers=headers, params=querystring)

        print(prediction_data.text)

        prediction = Predictions(date=formated_today_date, prediction=prediction_data.text )
        db.session.add(prediction)
        db.session.commit()

        with open("json.json", "w") as f:
            try:
                f.write(prediction_data.text)
            except Exception as exc:
                print(str(exc))
                f.write(prediction_data.content)

        return render_template("prediction/predict.html")

def processed_data(data):
    return data



# data_format
# 7:{22 items
# "id":33420
# "federation":"UEFA"
# "odds":{6 items
# "1":2.72
# "2":2.404
# "12":1.293
# "1X":1.47
# "X2":1.385
# "X":2.986
# }
# "field_length":NULL
# "away_team":"Hapoel Rishon LeZion"
# "competition_name":"Liga Leumit"
# "start_date":"2018-10-12T14:00:00"
# "prediction":"1X"
# "market":"classic"
# "home_strength":0.507757404795487
# "probabilities":{6 items
# "1":0.379
# "2":0.299
# "12":0.678
# "1X":0.701
# "X2":0.621
# "X":0.322
# }
# "stadium_capacity":4932
# "is_expired":false
# "distance_between_teams":95
# "last_update_at":"2018-10-11T22:30:57.275000"
# "competition_cluster":"Israel"
# "status":"pending"
# "result":""
# "away_strength":0.490909090909091
# "field_width":NULL
# "home_team":"Maccabi Ahi Nazareth"
# "season":"2018 - 2019"
# }