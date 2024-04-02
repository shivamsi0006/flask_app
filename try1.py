# import json

# file=open('sample_data.json')

# reader=json.load(file)

# for i in range(0,10,5):
#     print(reader["data"][i])


from flask import Flask,request,jsonify

app=Flask(__name__)
@app.route('/home',methods=['GET'])
def home():
    name=request.args.get("name","shivam",int)
    
    return jsonify({"message":name})

if __name__=='__main__':
    app.run(debug=True)