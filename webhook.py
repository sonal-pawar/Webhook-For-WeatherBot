import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

#  Flask app should start in gloal layout

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    #  force :  when we specify force True then it won't work for checking MIME type. any MIME type converted into JSON
    # silent :  if incoming data is not in proper JSON format then it will fail without throwing an exception 
    print(json.dumps(req, indent=4))

# next step
# Extract parameter values  -> query the weather API -> construct response -> send to dialogflow

    res = makeResponse(req)
    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=06f070197b1f60e55231f8c46658d077')
    json_object  = r.json()
    weather = json_object['list']
    for i in  range(0,30):
        if date in weather[i]['dt_txt']:
            condition = weather[i]['weather'][0]['description']
            break
    speech = "The forcast for "+city+ " for "+date+" is  " + condition

    return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-weather-webhook"
    }


# dialogflow expects following things :
# {
    # "speech": "", : contains actual text response from server 
    # "display text":"", what to display on device screen
    # "source":""   source where we got the respone from
# }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("starting app on port %d port", port)
    app.run(debug=False, port=port, host='0.0.0.0')
