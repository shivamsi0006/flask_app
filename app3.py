#  {"files" : [ {"file_name":  "foo.json", "file_data": {"key": "value"} }, {"file_name":  "foo.txt", "file_data": "any text data" }, {"file_name":  "foo.csv", "file_data": { "column": ["name", "surname"], "values": [["richard", "jones"], ["john", "doe"]] } } ] } 

from flask import Flask,request,jsonify
import json
import csv
app=Flask(__name__)


@app.route('/file',methods=['POST'])
def file():
    data=[]
    file_info={}
    dict_data=request.get_json()
    for i in dict_data["files"]:
        if i["file_name"].endswith(".json"):
            f=open("foo.json","w")
            json.dump(i["file_data"],f)
        if i["file_name"].endswith(".csv"):
            f=open("foo.csv","w")
            writer=csv.writer(f)
            writer.writerow(i["file_data"]["column"])
            writer.writerows(i["file_data"]["values"])
        if i["file_name"].endswith(".txt"):
            file =open('foo.txt',"w")
            file.write(i["file_data"])
        file_info={"file_name":i["file_name"],"location":f"/home/ca/Desktop/CloudAnalogy/CA/practice/{i['file_name']}"}
        data.append(file_info)

            
    return jsonify({"files":data})


if __name__=="__main__":
    app.run(debug=True)