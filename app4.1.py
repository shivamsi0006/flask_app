from flask import Flask
import asyncio

app=Flask(__name__)

@app.route('/asy',methods=["POSt"])
def asy():
    pass




if __name__=='__main__':
    app.run(debug=True)