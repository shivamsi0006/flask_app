from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///infoo.sqlite3"

db=SQLAlchemy(app)

class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    role=db.Column(db.String(200))
    email=db.Column(db.String(200),unique=True)
    password=db.Column(db.String(200))
    
    def __repr__(self):
        return f"{self.id}"

class Notes(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    User_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    note_name=db.Column(db.String(200))
    description=db.Column(db.Text)
    user=db.relationship("User",backref=db.backref("notes",lazy=True))
    
    def __repr__(self):
        return f"{self.User_id}"
    
def token_decode():
    header=request.headers.get("Authorization")
    decode=jwt.decode(header,"stringsecret",algorithms="HS256")
    return decode



@app.route('/register',methods=['POST'])
def register():
    name=request.get_json().get('name')
    email=request.get_json().get('email')
    password=request.get_json().get('password')
    verify=User.query.filter_by(email=email).first()
    if verify:
        return jsonify({"message":"user already exist"})
    query=User(name=name,email=email,password=password,role="customer")
    db.session.add(query)
    db.session.commit()
    return jsonify({"message":"user register successfully"})

@app.route('/signin',methods=['POST'])
def signin():
    email=request.get_json().get('email')
    password=request.get_json().get('password')
    verify= User.query.filter_by(email=email).first()
    if not verify:
        return jsonify({"message":"user does not exit"})
    if password==verify.password:
        data={"role":verify.role,"id":verify.id}
        token=jwt.encode(data,"stringsecret",algorithm='HS256')
        return jsonify({"access_token": token})
    return jsonify({"message": "password doest not match"})

@app.route('/createnote',methods=['POST'])
def createnote():
    decode=token_decode()
    note_name=request.get_json().get('note_name')
    description=request.get_json().get('description')
    print(decode)
    query=Notes(note_name=note_name,description=description,User_id=decode["id"])
    db.session.add(query)
    db.session.commit()
    return jsonify({"message":"note_created suceesfully"})

@app.route('/listnote',methods=['GET'])
def listnote():
    decode=token_decode()
    query=Notes.query.filter_by(User_id=decode["id"]).all()
    data=[]
    for i in query:
        d1={}
        d1={"note_name":i.note_name,
            "description":i.description
            }
        data.append(d1)
    print(data)
    return jsonify({"message":data})

@app.route('/update/<int:id>',methods=['PUT'])
def update(id):
    decode=token_decode()
    query=Notes.query.filter_by(User_id=decode["id"]).all()

    note_id=[note.id for note in query]
    if id in note_id:
        query2=Notes.query.filter_by(id=id).first()
        query2.id=id
        query2.note_name=request.get_json().get('note_name')
        query2.description=request.get_json().get('description')
        db.session.commit()
        return jsonify({"message":"update sucessfully"})
    return jsonify({"message":"not allowed for update "})

@app.route('/delete/<int:id>',methods=['DELETE'])
def delete_note(id):
    decode=token_decode()
    role=decode["role"]
    if role=="admin":
        query=Notes.query.filter_by(id=id).first()
        if query:
            db.session.delete(query)
            db.session.commit()
            return jsonify({"message":"note delete sucessfully"})
        return jsonify({"message":"note not found"})
    return jsonify({"message":"only admin can delete "})




if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)