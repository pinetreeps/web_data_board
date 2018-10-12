# _*_ coding:utf-8 _*_
# Filename: app.py
# Author: pang song
# python 3.6
# Date: 2018/08/06
# flask 展示地图
from flask import Flask,request,make_response,render_template
from flask_bootstrap import Bootstrap

import config, utils


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def hello_world():
    return 'Hello World!'

# @app.route('/index')
# def index():
#     return 'Hello index !'
#
# @app.route('/test1')
# def test1():
#     return render_template('index01.html')
# 读设备取监控（散点图）数据
device_monitor_data = utils.get_device_monitor_data(config.device_monitor_data)

@app.route('/test2')
def test2():
    return render_template('index02.html',
                           device_monitor_data=device_monitor_data,
                           department_name=config.department_name,
                           monitoring_coverage_rate=config.monitoring_coverage_rate,
                           avg_device_using_rate=config.avg_device_using_rate,
                           running_effective_time_year=config.running_effective_time_year,
                           shared_service_time_year=config.shared_service_time_year,
                           pie_data=config.pie_data)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8090, debug=True)
    app.run(port=8090,debug=True)