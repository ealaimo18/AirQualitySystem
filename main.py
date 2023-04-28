from flask import Flask, render_template, request, redirect
import os
import sqlite3, random
from datetime import datetime
from twilio.rest import Client

app = Flask('app')
app.secret_key = "things"

@app.route('/', methods=['GET', 'POST'])
def home():
    temp = 0
    humid = 0
    pm_inside = 0
    pm_outside = 0
    return render_template("index.html", temp=temp, humid=humid, pm_inside=pm_inside, pm_outside=pm_outside)

@app.route('/registerDevice', methods=['GET', 'POST'])
def registerDevice():
    if request.method == 'POST':
        id = request.form["device_id"]
        name = request.form["name"]
        lat = request.form["lat"]
        long = request.form["long"]
        connection = sqlite3.connect("myDatabase.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("INSERT INTO device (id, name, lat, long) VALUES (?, ?, ?, ?)", (id, name, lat, long))
        connection.commit()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def textSignUp():
    # Set environment variables for your credentials
    # Read more at http://twil.io/secure
    if request.method == 'POST':
        phone = request.form['phone']
    account_sid = "AC14a3f3132166d5d7afeb46621518c849"
    auth_token = "2dfd6c6e1868ab9567e8e239757a73d9"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
      body="Test this works",
      from_="+18776790836",
      to= phone
    #   to="+14846273900"
    )
    #print("text message sid", message.sid)
    return redirect('/')

@app.route('/map', methods=['GET', 'POST'])
def map():

    #fetch data points
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM DATA")
    points = cursor.fetchall()
    connection.commit()

    list = []

    # create list for a dictionary of each data point
    for point in points:
        data = {"temperature": point['temp'],
                 "humidity": point['humid'],
                 "pm_2_5":  point['pm_2_5'],
                 "aqi_2_5":  point['aqi_2_5'],
                 "pm_10":  point['pm_10'],
                 "aqi_10":  point['aqi_10'],
                 "lat":  point['lat'],
                 "long":  point['long']}    
        list.append(data)
   
    print(list)
    return render_template("home.html")

app.run(host='0.0.0.0', port=8080, debug=True)