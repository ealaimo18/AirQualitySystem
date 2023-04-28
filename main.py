from flask import Flask, render_template, request, redirect, jsonify
import os
import sqlite3, random
from datetime import datetime
from twilio.rest import Client


app = Flask('app')
app.secret_key = "things"

#global variables
phone = 0

# def test():
#     print("enters test")
#     #send texts with thresholds
#     aqi_10 = 110
#     aqi_2_5 = 0
#     if phone != 0:
#         # if aqi_2_5 or aqi_10 > 51 and aqi_2_5 or aqi_10 < 100:
#         #         message = "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."
#         #         sendText(phone, message)

#         # if aqi_2_5 or aqi_10 > 101 and aqi_2_5 or aqi_10 < 150:
#         #         message = "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
#         #         sendText(phone, message)

#         # if aqi_2_5 or aqi_10 > 151 and aqi_2_5 or aqi_10 < 200:
#         #         message = "ALERT! Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."
#         #         sendText(phone, message)
            
#         # if aqi_2_5 or aqi_10 > 201 and aqi_2_5 or aqi_10 < 300:
#         #         message = "HEALTH ALERT: The risk of health effects is increased for everyone."
#         #         sendText(phone, message)
            
#         # if aqi_2_5 or aqi_10 > 300:
#         #         message = "HEALTH WARNING of EMERGENCY CONDITIONS: everyone is more likely to be affected."
#         #         sendText(phone, message)
#     return
@app.route('/', methods=['GET', 'POST'])
def home():
    temp = 0
    humid = 0
    pm_2_5 = 0
    pm_10 = 0
    aqi_2_5 = 0
    aqi_10 = 0
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
        cursor.execute("SELECT * FROM device WHERE id = ?", (device_id,));
        device = cursor.fetchone()
        lat = device['lat'] 
        long = device['long']
        cursor.execute("INSERT into data (device_id, temp, humid, pm_2_5, pm_10, aqi_2_5, aqi_10, lat, long) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (device_id, temp, humid, pm_2_5, pm_10, aqi_2_5, aqi_10, lat, long))
        connection.commit()
        connection.close()

        #send texts with thresholds
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





    return render_template("index.html", temp=temp, humid=humid, pm_2_5 = pm_2_5, pm_10= pm_10,aqi_2_5 = aqi_2_5, aqi_10 = aqi_10 )

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
        data = {"temperature": point['temp'],
                 "humidity": point['humid'],
                 "pm_2_5":  point['pm_2_5'],
                 "aqi_2_5":  point['aqi_2_5'],
                 "pm_10":  point['pm_10'],
                 "aqi_10":  point['aqi_10'],
                 "lat":  point['lat'],
                 "long":  point['long']}    
        list.append(data)
   
    #print(list)
    return render_template("home.html",  points=jsonify(list))




app.run(host='0.0.0.0', port=8080, debug=True)
