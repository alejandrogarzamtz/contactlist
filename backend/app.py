from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)

CORS(app)
# Base de datos en memoria
contactos = []

@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    return jsonify(contactos), 200

@app.route("/api/contacts", methods=["POST"])
def add_contact():
    data = request.get_json()
    
    # Verificar si Flask recibe la solicitud correctamente
    print("Solicitud recibida:", data)

    if not data:
        return jsonify({"error": "No se recibió ningún dato"}), 400

    new_contact = {
        "id": str(uuid.uuid4()),
        "nombre": data.get("nombre"),
        "apellido": data.get("apellido"),
        "telefono": data.get("telefono"),
        "correo": data.get("correo"),
        "calle": data.get("calle"),
        "ciudad": data.get("ciudad"),
        "estado": data.get("estado"),
        "empresa": data.get("empresa"),
        "cargo": data.get("cargo"),
        "notas": data.get("notas"),
        "fecha_cumple": data.get("fecha_cumple")
    }

    contactos.append(new_contact)
    print("Contacto agregado:", new_contact)  # 🔍 Ver si el contacto realmente se guarda

    return jsonify({"message": "Contacto agregado", "contact": new_contact}), 201


@app.route("/api/contacts/<id>", methods=["PATCH"])
def update_contact(id):
    contact = next((c for c in contactos if c["id"] == id), None)
    if not contact:
        return jsonify({"error": "Contacto no encontrado"}), 404
    
    data = request.get_json()
    for key, value in data.items():
        if key in contact:
            contact[key] = value
    
    return jsonify({"message": "Contacto actualizado", "contact": contact}), 200

@app.route("/api/contacts/<id>", methods=["DELETE"])
def delete_contact(id):
    global contactos
    contactos = [c for c in contactos if c["id"] != id]
    return jsonify({"message": "Contacto eliminado"}), 200

@app.route("/api/contacts/<id>", methods=["GET"])
def get_contact(id):
    contact = next((c for c in contactos if c["id"] == id), None)
    if not contact:
        return jsonify({"error": "Contacto no encontrado"}), 404
    return jsonify(contact), 200

if __name__ == "__main__":
    app.run(debug=True)
