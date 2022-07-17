import json 
from sqlalchemy.orm import backref, deferred, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, DateTime, String, Enum, ForeignKey, Boolean
from flask_sqlalchemy  import SQLAlchemy

Base = declarative_base()
db = SQLAlchemy()



class Doctor(Base):
  __tablename__ = "doctor"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  appointments = relationship("Appointment")

  def to_json(self):
    return {
      'id': self.id,
      'name': self.name
    }

class Appointment(Base):
  __tablename__ = "appointment"
  id = Column(Integer, primary_key=True)
  doctor_id = Column(Integer, ForeignKey("doctor.id"))
  patient_first_name = Column(String)
  patient_last_name = Column(String)
  datetime = Column(DateTime)
  kind = Column(Enum("New Patient", "Follow-up",), default="New Patient")
  doctor = relationship("Doctor")
  deleted = Column(Boolean)

  def valid(self):
    same_time_count = db.session.query(Appointment).filter(datetime == self.datetime)\
      .filter(doctor_id == self.doctor_id).filter(deleted == 0).count()
    if same_time_count >= 3:
      return false

    minute = self.datetime.minute
    if (minute%15) != 0:
      return false
    return true 