

from flask import jsonify, request, abort
from models import Doctor


# @app.route('/doctors', methods=["GET"])
# def get_all_doctors():
#   doctors = Doctor.query.all()

# @app.route('/doctor/<int:id>', methods=["GET"])
# def get_doctor(id):
#   doctor = Doctor.query.get(id)
#   if doctor is None:
#     abort(404)
#   return jsonify(doctor.to_json())