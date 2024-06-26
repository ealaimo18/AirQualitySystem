from flask import Flask, render_template, request, redirect, jsonify
import os
import json
import sqlite3, random
from datetime import datetime
from twilio.rest import Client


app = Flask('app')
app.secret_key = "things"

#global variables
phone = 0
temp = 0
humid= 0
pm_2_5  = 0 
pm_10 = 0
aqi_2_5 = 0
aqi_10 = 0

@app.route('/', methods=['GET', 'POST'])
def home():
    
    global temp
    global humid
    global pm_2_5
    global pm_10
    global aqi_2_5
    global aqi_10

     #fetch data points
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM DATA")
    points = cursor.fetchall()
    connection.commit()
    connection.close()

    list = []
    # create list for a dictionary of each data point
    for point in points:
        data = {"temp": point['temp'],
                "humid": point['humid'],
                "pm_2_5":  point['pm_2_5'],
                "aqi_2_5":  point['aqi_2_5'],
                "pm_10":  point['pm_10'],
                "aqi_10":  point['aqi_10'],
                "lat":  point['lat'],
                "long":  point['long']}    
        list.append(data)
        #close connection
        connection.close()

    if request.method == 'POST':
        content = request.get_json()
        temp = content['temperature']
        humid = content['humidity']
        pm_2_5 = content['pm_2_5']
        pm_10 = content['pm_10']
        aqi_2_5 = content['aqi_2_5']
        aqi_10 = content['aqi_10']
        device_id = content['device_id']

        #insert into database
        connection = sqlite3.connect("myDatabase.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()


        #inserting data collected to db 
        cursor.execute("SELECT * FROM device WHERE id = ?", (device_id,));
        device = cursor.fetchone()
        lat = device['lat'] 
        long = device['long']
        cursor.execute("INSERT into data (device_id, temp, humid, pm_2_5, pm_10, aqi_2_5, aqi_10, lat, long) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (device_id, temp, humid, pm_2_5, pm_10, aqi_2_5, aqi_10, lat, long))
        cursor.execute("")
        connection.commit()
        connection.close()

        aqi_10 = 72
        #send texts with thresholds
        print(phone)
        if phone != 0:
            if  aqi_10 > 51 and aqi_10 < 100:
                message = "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."
                sendText(phone, message)

            if  aqi_2_5 or aqi_10 > 101 and aqi_2_5 or aqi_10 < 150:
                message = "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
                sendText(phone, message)

            if  aqi_10 > 151 and aqi_10 < 200:
                message = "ALERT! Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."
                sendText(phone, message)
            
            if aqi_10 > 201 and aqi_10 < 300:
                message = "HEALTH ALERT: The risk of health effects is increased for everyone."
                sendText(phone, message)
            
            if aqi_10 > 300:
                message = "HEALTH WARNING of EMERGENCY CONDITIONS: everyone is more likely to be affected."
                sendText(phone, message)
        return render_template("index.html", temp=temp, humid=humid, pm_2_5 = pm_2_5, pm_10= pm_10,aqi_2_5 = aqi_2_5, aqi_10 = aqi_10, points=json.dumps(list) )

    return render_template("index.html", temp=temp, humid=humid, pm_2_5 = pm_2_5, pm_10= pm_10,aqi_2_5 = aqi_2_5, aqi_10 = aqi_10, points=json.dumps(list) )

        # print(content['manue'])
        # f = open("demofile3.txt", "a")
        # f.write(content['manue'])
        # f.close()

def sendText(phone, message):
    # Set environment variables for your credentials
    # Read more at http://twil.io/secure
    if request.method == 'POST':
        phone = request.form['phone']
    account_sid = "AC14a3f3132166d5d7afeb46621518c849"
    auth_token = "2dfd6c6e1868ab9567e8e239757a73d9"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
      body=message,
      from_="+18776790836",
      to= phone
    )
    #print("text message sid", message.sid)
    return redirect('/')

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
        connection.close()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def textSignUp():
    # Set environment variables for your credentials
    # Read more at http://twil.io/secure
    global phone
    if request.method == 'POST':
        phone = request.form['phone']
    account_sid = "AC14a3f3132166d5d7afeb46621518c849"
    auth_token = "2dfd6c6e1868ab9567e8e239757a73d9"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
      body="Congrats you've registered for texts!",
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
    connection.close()

    list = []
    # create list for a dictionary of each data point
    for point in points:
        data = {"temp": point['temp'],
                 "humid": point['humid'],
                 "pm_2_5":  point['pm_2_5'],
                 "aqi_2_5":  point['aqi_2_5'],
                 "pm_10":  point['pm_10'],
                 "aqi_10":  point['aqi_10'],
                 "lat":  point['lat'],
                 "long":  point['long']}    
        list.append(data)
   
    #print(list)
    return render_template("home.html",  points=json.dumps(list))




app.run(host='0.0.0.0', port=5000, debug=True)

