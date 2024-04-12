from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
  return render_template('home.html')

@app.route("/sign_in")
def sign_in():
  return render_template('sign_in.html')

@app.route("/sign_up")
def sign_up():
  return render_template('sign_up.html')

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/contact")
def contact():
  return render_template('contact.html')

@app.route("/services")
def services():
  return render_template('services_page.html')

@app.route("/services/ead")
def ead():
  return render_template('ead.html')

@app.route("/services/express_parcel")
def express_parcel():
  return render_template('express_parcel.html')

@app.route("/services/ptf")
def ptf():
  return render_template('ptf.html')

@app.route("/services/scs")
def scs():
  return render_template('scs.html')

@app.route("/services/truck_freight")
def truck_freight():
  return render_template('truck_freight.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
