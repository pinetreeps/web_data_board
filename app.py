# _*_ coding:utf-8 _*_
# Filename: app.py
# Author: pang song
# python 3.6
# Date: 2018/08/06
# flask 展示地图
from flask import Flask,request,make_response,render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
def index():
    return 'Hello index !'

@app.route('/test1')
def test1():
    return render_template('index01.html')

@app.route('/test2')
def test2():
    return render_template('index02.html')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8090, debug=True)
    app.run(port=8090,debug=True)