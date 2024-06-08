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

@app.route('/delete_shipment/<id>', methods=['GET', 'POST'])
def delete_shipment(id):
    try:
        shipment = shipments_ref.document(id)
        shipment.delete()
        flash('Shipment deleted successfully', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
    return redirect('/view_shipments')


@app.route('/add_shipment', methods=['GET', 'POST'])
def add_shipment():
  if request.method == 'POST':
    # Retrieve form data
    ship_name = request.form.get('shipName')
    ship_phone = request.form.get('shipPhone')
    ship_address = request.form.get('shipAddress')
    ship_email = request.form.get('shipEmail')
    ship_gst = request.form.get('shipGST')

    rec_name = request.form.get('recName')
    rec_phone = request.form.get('recPhone')
    rec_address = request.form.get('recAddress')
    rec_email = request.form.get('recEmail')
    rec_pin = request.form.get('recPin')

    ship_type = request.form.get('shipType')
    unit_count = request.form.get('unitCount')
    box_count = request.form.get('boxCount')
    po_number = request.form.get('poNumber')
    po_expiry = request.form.get('poExpiry')
    invoice_number = request.form.get('invoiceNumber')
    invoice_value = request.form.get('invoiceValue')
    amount_collected = request.form.get('amountCollected')
    cn_number = request.form.get('cnNumber')
    apt_number = request.form.get('aptNumber')
    apt_date = request.form.get('aptDate')

    ass_branch = request.form.get('ass_branch')

    client = request.form.get('client')
    agent = request.form.get('agent')
    branch_man = request.form.get('branchMan')
    driver = request.form.get('driver')
    
    container = request.form.get('container')
    
    date = request.form.get('date')
    time = request.form.get('time')
    location = request.form.get('location')
    status = request.form.get('status')
    
    packages = []
    for qty, piece_type, description, length, width, height, weight in zip(
        request.form.getlist('qty[]'), 
        request.form.getlist('pieceType[]'), 
        request.form.getlist('description[]'), 
        request.form.getlist('length[]'), 
        request.form.getlist('width[]'), 
        request.form.getlist('height[]'), 
        request.form.getlist('weight[]')
    ):
      packages.append({
          'qty': qty,
          'piece_type': piece_type,
          'description': description,
          'length': length,
          'width': width,
          'height': height,
          'weight': weight
      })
    shipment_data = {
      'shipper_name': ship_name,
      'shipper_phone': ship_phone,
      'shipper_address': ship_address,
      'shipper_email': ship_email,
      'shipper_gst': ship_gst,
      'receiver_name': rec_name,
      'receiver_phone': rec_phone,
      'receiver_address': rec_address,
      'receiver_email': rec_email,
      'shipment_type': ship_type,
      'unit_count': unit_count,
      'box_count': box_count,
      'po_number': po_number,
      'po_expiry': po_expiry,
      'invoice_number': invoice_number,
      'invoice_value': invoice_value,
      'amount_collected': amount_collected,
      'cn_number': cn_number,
      'appointment_number': apt_number,
      'container': container,
      'packages': packages
    }

    # Assuming you have a Firestore collection called 'shipments'
    shipments_ref.add(shipment_data)
    return redirect('/view_shipments')

  return render_template('add_shipment.html')

@app.route('/view_shipments', methods=['GET', 'POST'])
def view_shipments():
  status = request.args.get('status')
  shipper_name = request.args.get('shipper_name')
  receiver_name = request.args.get('receiver_name')
  date_start = request.args.get('date_start')
  date_end = request.args.get('date_end')
  page = int(request.args.get('page', 1))
  per_page = 10

  query = shipments_ref

  if status:
      query = query.where('status', '==', status)
  if shipper_name:
      query = query.where('shipper_name', '==', shipper_name)
  if receiver_name:
      query = query.where('receiver_name', '==', receiver_name)
  if date_start:
      query = query.where('date_created', '>=', date_start)
  if date_end:
      query = query.where('date_created', '<=', date_end)

  # Fetch documents and include the document ID in the data
  shipments = []
  for doc in query.stream():
      shipment = doc.to_dict()
      shipment['id'] = doc.id
      shipments.append(shipment)

  total_shipments = len(shipments)
  total_pages = (total_shipments + per_page - 1) // per_page
  shipments = shipments[(page-1)*per_page:page*per_page]

  return render_template('view_shipments.html', 
                         shipments=shipments, 
                         page=page, 
                         total_pages=total_pages)

@app.route('/view_shipment/<id>')
def view_shipment(id):
    shipment = shipments_ref.document(id).get()
    if shipment.exists:
        return render_template('shipment.html', shipment=shipment.to_dict())
    else:
        return 'Shipment not found', 404

@app.route('/view_shipments/edit/<id>', methods=['GET', 'POST'])
def edit_shipment(id):
  shipment_ref = shipments_ref.document(id)
  shipment = shipment_ref.get()
  if not shipment.exists:
      return 'Shipment not found', 404

  if request.method == 'POST':
      updated_data = {
          'shipper_name': request.form.get('shipperName'),
          'shipper_phone': request.form.get('shipperPhone'),
          'shipper_address': request.form.get('shipperAddress'),
          'shipper_email': request.form.get('shipperEmail'),
          'shipper_gst': request.form.get('shipperGST'),
          'receiver_name': request.form.get('receiverName'),
          'receiver_phone': request.form.get('receiverPhone'),
          'receiver_address': request.form.get('receiverAddress'),
          'receiver_email': request.form.get('receiverEmail'),
          'shipment_type': request.form.get('shipmentType'),
          'unit_count': request.form.get('unitCount'),
          'box_count': request.form.get('boxCount'),
          'po_number': request.form.get('poNumber'),
          'po_expiry': request.form.get('poExpiry'),
          'invoice_number': request.form.get('invoiceNumber'),
          'invoice_value': request.form.get('invoiceValue'),
          'amount_collected': request.form.get('amountCollected'),
          'cn_number': request.form.get('cnNumber'),
          'appointment_number': request.form.get('appointmentNumber'),
          'container': request.form.get('container'),
          'packages': []
      }
      for qty, piece_type, description, length, width, height, weight in zip(
          request.form.getlist('qty[]'), 
          request.form.getlist('pieceType[]'), 
          request.form.getlist('description[]'), 
          request.form.getlist('length[]'), 
          request.form.getlist('width[]'), 
          request.form.getlist('height[]'), 
          request.form.getlist('weight[]')
      ):
          updated_data['packages'].append({
              'qty': qty,
              'piece_type': piece_type,
              'description': description,
              'length': length,
              'width': width,
              'height': height,
              'weight': weight
          })
      shipment_ref.update(updated_data)
      return redirect(url_for('view_shipments'))

  return render_template('edit_shipment.html', shipment=shipment.to_dict(), id=id)

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
              return redirect('/view_shipments')
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
