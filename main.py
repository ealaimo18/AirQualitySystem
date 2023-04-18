from flask import Flask, render_template, request, redirect

app = Flask('app')
app.secret_key = "things"

@app.route('/')
def home():
    temp = 0
    humid = 0
    pm_inside = 0
    pm_outside = 0
    return render_template("index.html", temp=temp, humid=humid, pm_inside=pm_inside, pm_outside=pm_outside)


app.run(host='0.0.0.0', port=8080, debug=True)