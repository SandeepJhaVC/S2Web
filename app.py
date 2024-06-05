from flask import Flask, flash, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db, auth, firestore

from models import Shipment

cred = credentials.Certificate('static/s2log-f75ab-firebase-adminsdk-i95uu-5954bc85a9.json')
firebase_admin.initialize_app(cred)

rt=db.reference(url='https://s2log-f75ab-default-rtdb.asia-southeast1.firebasedatabase.app')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asbeccdreeft'

fs = firestore.client()
shipments_ref = fs.collection('shipments')


@app.route("/")
def hello_world():
  return render_template('home.html')

@app.route('/add_shipment', methods=['GET', 'POST'])
def add_shipment():
    if request.method == 'POST':
        date_of_shipment = request.form.get('date_of_shipment')
        date_of_delivery = request.form.get('date_of_delivery')
        vehicle_type = request.form.get('vehicle_type')
        vehicle_no = request.form.get('vehicle_no')
        employee = request.form.get('employee')
        client = request.form.get('client')

        shipment = {
            'date_of_shipment': date_of_shipment,
            'date_of_delivery': date_of_delivery,
            'vehicle_type': vehicle_type,
            'vehicle_no': vehicle_no,
            'employee': employee,
            'client': client
        }
        shipments_ref.add(shipment)
        return redirect('/view_shipments')

    return render_template('add_shipment.html')

@app.route('/view_shipments')
def view_shipments():
    shipments = []
    for doc in shipments_ref.stream():
        shipment = doc.to_dict()
        if shipment is not None:
            shipment['id'] = doc.id  # Add the document ID to the shipment dictionary
            shipments.append(shipment)
            print(shipment['id'])  # Print the ID to debug
    return render_template('view_shipments.html', shipments=shipments)

@app.route('/delete_shipment/<id>', methods=['GET', 'POST'])
def delete_shipment(id):
    try:
        shipment = shipments_ref.document(id)
        shipment.delete()
        flash('Shipment deleted successfully', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
    return redirect('/view_shipments')

@app.route("/admin/sign_in", methods=['GET','POST'])
def login():
  if request.method == "POST":
    email = request.form.get('email')
    password = request.form.get('password')

    try:
      # Retrieve user data from Firebase Realtime Database
      users = rt.get()
      print(users)
      for user_id, user_data in users.items():
          if user_data['email'] == email and user_data['password'] == password:
              flash("Logged in successfully", category="success")
              return redirect('/admin')
      flash("Invalid email or password", category="error")
    except Exception as e:
      flash(f"Error: {e}", category="error")

  return render_template('sign_in.html')

@app.route("/admin/sign_up", methods=['GET','POST'])
def sign_up():
  if request.method == "POST":

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')

    if len(name) == 0:
      flash("Name is required", category="error")
    elif len(email) < 2:
      flash("Email format is not correct", category="error")
    elif password != cpassword:
      flash("Passwords do not match", category="error")
    else:
      # Create user in Firebase Authentication
      try:
          user = auth.create_user(email=email, password=password)
          print(f"Successfully created user: {user.uid}")
      except Exception as e:
          flash(f"Error creating user: {e}", category="error")
          return render_template('sign_up.html')

      # Save user data to Firebase Realtime Database
      user = {
        "email":email,
        "name":name,
        "password":password
      }
      rt.push(user)

      flash("Account created", category="success")
      return redirect("/sign_in")

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
