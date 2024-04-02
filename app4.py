
# Task 1: 

# Use httpx to fetch the expected gender for a list of persons from the provided API (https://api.genderize.io?name={person_name}) and store the results in a CSV file. The CSV format should have columns "Name" and "Gender."


from flask import Flask ,jsonify
import requests

app=Flask(__name__)

def api(url):
    response=requests.get(url)
    data=response.json()
    return data


@app.route("/store",methods=['POST'])
def store():
    persons=["arjun","anjali","satish","sakshi"]
    file=open("app4.csv","a")
    for person in persons:
        url=f"https://api.genderize.io?name={person}"
        data=api(url)
        file=open("app4.csv","a")
        file.write(f"{data['name']} , {data['gender']}\n")
    file.close()
    return jsonify({"message":"data write sucessfully"})

if __name__=="__main__":
    app.run(debug=True)
