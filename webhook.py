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
    api_key = "8b316cbdc31b46e8ea8aca2e73ed3377"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city 

    r = requests.get(complete_url) 
    json_object  = r.json()
    if json_object["cod"] != "404": 

        # store the value of "main" 
        # key in variable y 
        y = json_object["main"] 

        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = y["temp"] 

        # store the value corresponding 
        # to the "pressure" key of y 
        current_pressure = y["pressure"] 

        # store the value corresponding 
        # to the "humidity" key of y 
        current_humidiy = y["humidity"] 

        # store the value of "weather" 
        # key in variable z 
        z = json_object["weather"] 

        # store the value corresponding 
        # to the "description" key at 
        # the 0th index of z 
        weather_description = z[0]["description"] 

        # print following values 
        print(" Temperature (in kelvin unit) = " +
                        str(current_temperature) +
            "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
            "\n humidity (in percentage) = " +
                        str(current_humidiy) +
            "\n description = " +
                        str(weather_description)
                        ) 
        description = " Temperature (in kelvin unit) = " + str(current_temperature) + "\n atmospheric pressure (in hPa unit) = " + str(current_pressure) + "\n humidity (in percentage) = " +  str(current_humidiy) +"\n description = " + str(weather_description)
                    
    else: 
        print(" City Not Found ") 

    speech = "The forcast for "+city+ " for "+date+" is  " + description

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
    print("starting app on port {} port".format(port))
    app.run(debug=True, port=port, host='127.0.0.1')
