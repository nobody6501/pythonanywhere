
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import os
from sqlalchemy import create_engine
from flask import jsonify, request, abort
import json 
from sqlalchemy.orm import backref, deferred, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, DateTime, String, Enum, ForeignKey
from .models import db, Doctor, Appointment
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

Session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=db))
session = Session

@app.before_first_request
def create_table():
    db.create_all()


@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/doctors', methods=["GET"])
def get_all_doctors():
  doctors = db.session.query(Doctor).all()
  return jsonify([doctor.to_json() for doctor in doctors])


@app.route('/doctor/<int:id>', methods=["GET"])
def get_doctor(id):
  doctor = Doctor.query.get(id)
  if doctor is None:
    abort(404)
  return jsonify(doctor.to_json())

@app.route('/create', methods=["POST"])
def create_appointment():
  if not request.json:
    abort(400)
  appointment = Appointment(
      doctor_id = request.json.get('doctor_id'),
      patient_first_name = request.json.get('patient_first_name'),
      patient_last_name = request.json.get('patient_last_name'),
      datetime = request.json.get('datetime'),
      kind = request.json.get('kind'),
      deleted = 0,
  )

  if appointment.valid():

    db.session.add(appointment)
    db.session.commit()
    return json.dumps({"data": appointment}), 200
  else:
    return json.dumps({"error": "invalid input"}), 500


if __name__ == '__main__':
  doctor = Doctor(name='Testing tester')
  db.session.add(doctor)
  db.session.commit()
  app.run(debug=True)
