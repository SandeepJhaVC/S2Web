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

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
