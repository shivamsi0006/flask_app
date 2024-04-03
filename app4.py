
# Task 1: 

# Use httpx to fetch the expected gender for a list of persons from the provided API (https://api.genderize.io?name={person_name}) and store the results in a CSV file. The CSV format should have columns "Name" and "Gender."


from flask import Flask ,jsonify
import requests
import csv

app=Flask(__name__)

def api(url):
    response=requests.get(url)
    data=response.json()
    return data.get("gender")


@app.route("/store",methods=['POST'])
def store():
    persons=["arjun","anjali","satish","sakshi"]
    file=open("app4.csv","a")
    feildnames=["Name","Gender"]
    writer=csv.DictWriter(file,fieldnames=feildnames)
    writer.writeheader()
    for person in persons:
        url=f"https://api.genderize.io?name={person}"
        gender=api(url)
        writer.writerow({"Name":person,"Gender":gender})
    file.close()
    return jsonify({"message":"data write sucessfully"})

if __name__=="__main__":
    app.run(debug=True)
