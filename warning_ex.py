import requests

def main():
    t = 25
    p = 0
    h = 40
    pmt_2_5 = 23
    aqi_2_5 = 18
    pmt_10 = 72
    aqi_10 = 72
    url = 'http://161.253.92.155:5000/'
    myobj = {"temperature": str(t), 
                 "pressure": str(p),
                 "humidity": str(h),
                 "pm_2_5": str(pmt_2_5),
                 "aqi_2_5": str(aqi_2_5),
                 "pm_10": str(pmt_10),
                 "aqi_10": str(aqi_10), 
                 "device_id": 21}  #device id should be hard coded because it will never change with node
    x = requests.post(url, json = myobj)
    return

if __name__ == "__main__":
    main() 

