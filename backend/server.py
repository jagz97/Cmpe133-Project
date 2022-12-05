
import bcrypt
from flask import Flask, jsonify, request, session
from flask_session import Session
from flask_bcrypt import Bcrypt
import datetime
from config import ApplicationConfig
from models import db, User
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config.from_object(ApplicationConfig)


bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)




db.init_app(app)
with app.app_context():
    db.create_all()

@cross_origin()
@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    }) 



#######################################################
############Sample route for jsonified data############
###############to use with react######################


@app.route('/data')
def get_time():

    x = datetime.datetime.now()
    y = "here"
  
  
    # Returning an api for showing in  reactjs
    return {
        'Name':y, 
        "Age":"22",
        "Date":x, 
        "programming":"python"
        }

#######################################################
############         All function         ############
######################################################


@app.route("/register", methods=["POST","GET"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    user_exist = User.query.filter_by(email = email).first() is not None

    if user_exist:
        return jsonify({"error":"User already exist"}), 409
    
    h_pass = bcrypt.generate_password_hash(password)
    new_user = User(email = email, password= h_pass)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })


@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })


@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"

      
# Running app
if __name__ == '__main__':
    app.run(debug=True)
