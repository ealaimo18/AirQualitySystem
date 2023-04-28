import dweepy
import requests
import pandas as pd
import json
from pandas import json_normalize

url1 = 'https://api.waqi.info'
# Get token from:- https://aqicn.org/data-platform/token/#/
token = '94c92f71338f2df6fa3ccc16b91b6d7f8f628146'
box = '113.805332,22.148942,114.434299,22.561716' # polygon around HongKong via bboxfinder.com
url2=f'/map/bounds/?latlng={box}&token={token}'
my_data = pd.read_json("https://api.waqi.info/feed/here/?token=94c92f71338f2df6fa3ccc16b91b6d7f8f628146") 




o_pm_2_5 = int((my_data['data'][6]['pm25']['v']))
o_pm_10 = int((my_data['data'][6]['pm10']['v']))

#o_pm_2_5 = 2
#o_pm_10 = 2


msg = dweepy.get_latest_dweet_for('AQVS_Sensor')

print(msg)

pm_2_5 = int (msg[0]['content']['aqi_2_5'])
pm_10 = int (msg[0]['content']['aqi_10'])

h = int(msg[0]['content']['humidity'])

if(h>50):
     print("Humidity Level Too High, Pollution Data Might Be Inaccurate")
    

if ((pm_2_5> o_pm_2_5)or (pm_10> o_pm_10)):
    print("Open The Window: Indoor Pollution Higher than Outside")
else:
    print("Pollution Levels Lower than Outside")
