from flask import render_template,request
from flask import Flask
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route("/",methods=["GET" ,"POST"])
def index():
    #takes the user city name and search in the data base.
    if request.method  == "POST":

        city= request.form.get("search")
        weather_value=getting_weather_forecast(city)
        #passing the list of directories to the index page
        return render_template("index.html",values=weather_value)
    else:
        return render_template("index.html")
    

def getting_weather_forecast(city):

    #got the key from website
    api_key="67f7cbe9dcc941f91e9d0466ee3d40e9"
    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    responce=requests.get(url)

    #checking if the value of city is there or not.
    if responce.status_code == 200:
        return responce.json()
    else:
        return None
    

if __name__ == "__main__":
    app.run(debug=True)