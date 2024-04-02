# Q-3: Create Database Info with fields (user_id, title, body), Create API which call below API and store all data into database use requests library. api: https://jsonplaceholder.typicode.com/posts/ 

from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Info.sqlite3'
db=SQLAlchemy(app)

class Info(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    title=db.Column(db.Text)
    body=db.Column(db.Text)

    def __repr__(self):
        return f"{self.id}"
    
def api(url):
    response=requests.get(url)
    data=response.json()
    return data   


@app.route("/fetch",methods=['GET'])
def fetch():
    data=api('https://jsonplaceholder.typicode.com/posts/')
    for i in data:
        user_id=i["userId"]
        title=i["title"]
        body=i["body"]
        query=Info(user_id=user_id,title=title,body=body)
        db.session.add(query)
        db.session.commit()
    return({"message":"api fetch sucessfully"})

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
