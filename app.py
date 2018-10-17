# _*_ coding:utf-8 _*_
# Filename: app.py
# Author: pang song
# python 3.6
# Date: 2018/08/06
# flask 展示地图
import time
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

@app.route('/test1')
def test1():
    # 读设备取监控（散点图）数据
    device_monitor_data = utils.get_device_monitor_data(config.device_monitor_data)
    # 获取天气数据以及图片
    weather_data = utils.get_weather('beijing')
    weather_img_path = utils.get_weather_img_path(weather_data[1])
    return render_template('index02.html',
                           weather_data=weather_data,
                           weathre_img_path=weather_img_path,
                           device_monitor_data=device_monitor_data,
                           department_name=config.department_name,
                           monitoring_coverage_rate=config.monitoring_coverage_rate,
                           avg_device_using_rate=config.avg_device_using_rate,
                           running_effective_time_year=config.running_effective_time_year,
                           shared_service_time_year=config.shared_service_time_year,
                           pie_data=config.pie_data)


@app.route('/test2')
def test2():
    # 读取中心显示数据
    center_data = utils.get_center_data()
    # 读设备取监控（散点图）数据
    device_monitor_data = utils.get_device_monitor_data(utils.get_api_data(config.API_URL_DEVICE_MONITOR, config.device_monitor_data))

    # 读取bar1 监控覆盖率 vs 平均设备使用率
    MCR_vs_ADUR = utils.deal_api_data_for_bar1()

    # 读取bar2 年平均运行有效机时 vs 年平均共享服务机时
    RETY_vs_SSTY = utils.deal_api_data_for_bar2()
    # print(RETY_vs_SSTY[2])

    # 获取天气数据以及图片
    weather_data = utils.get_weather('beijing')
    weather_img_path = utils.get_weather_img_path(weather_data[1])
    return render_template('index02.html',
                           center_data=center_data,
                           weather_data=weather_data,
                           weathre_img_path=weather_img_path,
                           device_monitor_data=device_monitor_data,
                           department_name1=MCR_vs_ADUR[0],
                           monitoring_coverage_rate=MCR_vs_ADUR[1],
                           avg_device_using_rate=MCR_vs_ADUR[2],
                           department_name2=RETY_vs_SSTY[0],
                           running_effective_time_year=RETY_vs_SSTY[1],
                           shared_service_time_year=RETY_vs_SSTY[2],
                           pie_data=config.pie_data)

if __name__ == '__main__':
    # 线上
    app.run(host='0.0.0.0', port=8097, debug=True)
    # 本机
    # app.run(port=8090,debug=True)