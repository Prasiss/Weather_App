from flask import render_template,request
from flask import Flask
import requests,sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/",methods=["GET" ,"POST"])
def index():
    #takes the user city name and search in the data base.
    if request.method  == "POST":
        city= request.form.get("search")
        weather_value=getting_weather_forecast(city) 
        #trying to save the data into database
        if weather_value:
            temp= weather_value["main"]["temp"]
            #generate a background image based on temperature
            background_image = generate_background_image(temp)
            saving_data(weather_value)
        database_value=fetch_data()
        #passing the list of directories to the index page
        return render_template("index.html",values=weather_value,database_value=database_value,background_image=background_image)
    else:
        database_value= fetch_data()
        return render_template("index.html",database_value=database_value,)

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
    
def saving_data(value):
    #saving the data in th data base from the jason file
    conn=sqlite3.connect("search.db")

    cursor= conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Weather_details (id INTEGER PRIMARY KEY AUTOINCREMENT,City TEXT NOT NULL,Temperature REAL,
                   Pressure INTEGER,Humidity INTEGER,Visibility INTEGER)''')

    cursor.execute('''INSERT INTO Weather_details (City,Temperature,Pressure,Humidity,Visibility) VALUES (?,?,?,?,?)
                ''',(value["name"],value["main"]["temp"],value["main"]["pressure"],value["main"]["humidity"],value["visibility"]))
    conn.commit()

def fetch_data():

    #fetching the data from database
    conn=sqlite3.connect("search.db")
    conn.row_factory =sqlite3.Row
    cursor= conn.cursor()

    cursor.execute('''SELECT * FROM Weather_details''')
    rows=cursor.fetchall()

    conn.close()
    return rows

def generate_background_image(temperature):
    # This function can be used to generate a background image if needed
    if (temperature < 0):
        return "cold_background.jpg"
    elif (temperature < 20):
        return "cool_background.jpg"
    elif (temperature < 30):
        return "warm_background.jpg"
    else:
        return "hot_background.jpg"

if __name__ == "__main__":
    app.run(debug=True)
