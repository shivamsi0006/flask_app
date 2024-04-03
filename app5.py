from flask import Flask,request,jsonify
import json
app=Flask(__name__)

with open("sample_data.json") as f:
    sample_data=json.load(f)

@app.route("/filter",methods=['GET'])
def filter():
    filter_key=request.args.get("filter_key")
    filter_value=request.args.get("filter_value")
    page=request.args.get("page",1,int)
    per_page=request.args.get("per_page",10,int)


    filter_data=[items for items in sample_data["data"] if items.get(filter_key)==filter_value]

    start=(page-1)*per_page
    end=(start+per_page)
    total_items=len(filter_data)
    total_page=(total_items+per_page-1)//per_page
    
    if page<total_page:
        nextpage=page+1
    else:
        nextpage="None"

    response={
        "data":filter_data[start:end],
        "next_page":nextpage,
        "total_items":total_items,
        "total_page":total_page,
        "page":page,
        "per_page":per_page
    }

    return jsonify(response)


if __name__=='__main__':
    app.run(debug=True)



