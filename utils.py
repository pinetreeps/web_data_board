# _*_ coding:utf-8 _*_
# Filename: utils.py
# Author: pang song
# python 3.6
# Date: 2018/10/12

import requests
import re
import json

import config


def get_device_monitor_data(input_data):
    # xx = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9',
    #       'x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9']
    # yy = ['y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9',
    #       'y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9',
    #       'y0', 'y1', 'y2', 'y3']

    xx = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9',
          'x0', 'x1', 'x2', 'x3', 'x4']
    yy = ['y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9',
          'y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7']

    device_running_list = []
    device_standby_list = []
    device_shutdown_list = []
    device_no_use_list = []

    num_device = 0

    for yn in range(len(yy)):
        for xn in range(len(xx)):
            device = []
            # print(xn, yn)
            device.append(xn)
            device.append(yn)
            # print(num_device)
            # print(input_data[num_device])
            # print(input_data[num_device].get('value'))
            device.append(
                # u'设备名称：' + input_data[num_device].get('name') + u'<br> 资产编号：' + input_data[num_device].get('device_code'))
                u'设备名称：{dn} <br> 资产编号：{dc}'.format(dn=input_data[num_device].get('NAME'), dc=input_data[num_device].get('DEVICE_CODE')))
            if input_data[num_device].get('VALUE') == "0":
                device_running_list.append(device)
            elif input_data[num_device].get('VALUE') == "1":
                device_standby_list.append(device)
            elif input_data[num_device].get('VALUE') == "2":
                device_shutdown_list.append(device)
            # elif input_data[num_device].get('value') == "3":
            elif input_data[num_device].get('VALUE') == "-1":
                device_no_use_list.append(device)
            else:
                print("do nothing")
            num_device += 1
            if num_device >= len(input_data):
                return [device_running_list, device_standby_list, device_shutdown_list, device_no_use_list]
            # device.append(xn)
            # device.append(yn)
    return [[],[],[],[]]
    # print(device_running_list)
    # print(device_standby_list)
    # print(device_shutdown_list)
    # print(device_no_use_list)

#  获取网页内容
def getHTMLtext(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()  # 如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding  # r.apparent_encoding:根据网页内容分析出的编码方式
        return r.text
    except:
        print("爬取失败")
        return ("")

def get_weather(city_str):
    # url = "http://www.weather.com.cn/weather1d/101010100.shtml"
    url = "http://www.tianqi.com/{}/".format(city_str)
    # url = "http://qq.ip138.com/weather/beijing/"
    weather_data = [u'气温正常', u'多云', u'北风']

    whtml = getHTMLtext(url)
    # print(whtml)
    #  抓取数据区块的正则
    # w_info_pattern = re.compile("hour3data=(.*?)</script>", re.S)
    w_info_pattern = re.compile("<dd class=\"name\"><h2>.*?</div>", re.S)
    #  使用正则抓取数据区块
    w_info = w_info_pattern.findall(whtml)
    # print(w_info)
    try:
        temperature_pattern = re.compile("class=\"now\"><b>(.*?)</b>", re.S)
        weather_data[0] = temperature_pattern.findall(w_info[0])[0]

        weather_pattern = re.compile("<span><b>(.*?)</b>", re.S)
        weather_data[1] = weather_pattern.findall(w_info[0])[0]

        wind_pattern = re.compile(u"<b>风向：(.*?)</b>", re.S)
        weather_data[2] = wind_pattern.findall(w_info[0])[0]
    except Exception as e:
        print("get weather data error, ", repr(e))
    return weather_data


def get_weather_img_path(weather_str):
    if u'小雨' == weather_str:
        return 'static/images/leoweather/xiaoyu.png'
    elif u'大雨' == weather_str:
        return 'static/images/leoweather/dayu.png'
    elif u'多云' == weather_str:
        return 'static/images/leoweather/duoyun.png'
    elif u'晴' == weather_str:
        return 'static/images/leoweather/qing.png'
    elif u'阴' == weather_str:
        return 'static/images/leoweather/yin.png'
    elif u'中雨' == weather_str:
        return 'static/images/leoweather/zhongyu.png'
    else:
        return 'static/images/leoweather/duoyun.png'

def get_api_data(url, backup_data):
    # 发送get请求
    return_data = []
    try:
        # 获取返回的json数据转为字典
        data = requests.get(url).json()
        # print(data)
        if data.get('message') == 'succes' and data.get('status') == '0':
            return_data = data.get('result')
        else:
            print("api data message: {m}, status: {s}".format(m=data.get('message'), s=data.get('status')))
            return_data = backup_data
    except Exception as e:
        print("get api data error,{}".format(repr(e)))
        return_data = backup_data
    return return_data

def deal_api_data_for_bar1():
    '''
    为柱状图格式化数据1 监控覆盖率 vs 平均设备使用率
    :return: 三个列表组成的列表
    '''
    return_lists = [[],[],[]]
    monitoring_coverage_rate = get_api_data(config.API_URL_MONITORING_COVERAGE_RATE, config.BACKUP_DATA_MONITORING_COVERAGE_RATE)
    avg_device_using_rate = get_api_data(config.API_URL_AVG_DEVICE_USING_RATE, config.BACKUP_DATA_AVG_DEVICE_USING_RATE)

    for data1 in monitoring_coverage_rate:
        return_lists[0].append(data1.get('NAME'))
        return_lists[1].append(data1.get('VALUE'))
        for data2 in avg_device_using_rate:
            if data1.get('NAME') == data2.get('NAME'):
                return_lists[2].append(data2.get('VALUE'))
        if len(return_lists[1]) > len(return_lists[2]):
            return_lists[2].append(0)
    return return_lists

def deal_api_data_for_bar2():
    '''
    为柱状图格式化数据2 年平均有效机时 vs 共享机时（暂时无数据）
    :return:
    '''
    return_lists = [[],[],[]]
    running_effective_time = get_api_data(config.API_URL_RUNNING_EFFECTIVE_TIME, config.BACKUP_DATA_RUNNING_EFFECTIVE_TIME)
    shared_service_time = get_api_data(config.API_URL_SHARE_SERVICE_TIME, config.BACKUP_DATA_SHARE_SERVICE_TIME)
    # print(running_effective_time)
    print(shared_service_time)
    for data1 in running_effective_time:
        return_lists[0].append(data1.get('NAME'))
        return_lists[1].append(data1.get('VALUE'))
        for data2 in shared_service_time:
            if data1.get('NAME') == data2.get('NAME'):
                return_lists[2].append(data2.get('VALUE'))
        if len(return_lists[1]) > len(return_lists[2]):
            return_lists[2].append(0)
    return return_lists

def get_center_data():
    center_data = get_api_data(config.API_URL_CENTER_DISPLAY, config.BACKUP_DATA_CENTER_DISPLAY)
    # print(center_data)
    # print(type(center_data[0].get('监控覆盖率')))
    return_data = []
    return_data.append(round(center_data[0].get(u'监控覆盖率'),1))
    return_data.append(round(center_data[1].get(u'设备使用率'),1))
    return return_data


if __name__ == '__main__':

    print(get_center_data())
    # exit()

    # 测试3
    aa = get_api_data(config.API_URL_CENTER_DISPLAY, [])
    print(type(aa))
    print(aa)
    # exit()

    bb = get_api_data(config.API_URL_AVG_DEVICE_USING_RATE,[])
    print(len(bb))
    for b in bb:
        print(b)

    cc = get_api_data(config.API_URL_MONITORING_COVERAGE_RATE, [])
    print(len(cc))
    for c in cc:
        print(c)

    dd = deal_api_data_for_bar1()
    for d in range(len(dd[0])):
        print(d, dd[0][d], dd[1][d], dd[2][d])

    ee = deal_api_data_for_bar2()
    for e in range(len(ee[0])):
        print(e, ee[0][e], ee[1][e], ee[2][e])

    for e2 in ee:
        print(e2)

    exit()

    ff = get_api_data(config.API_URL_DEVICE_MONITOR, [])
    print(len(ff))
    # for f in ff:
    #     print(f,',')

    exit()





    # 测试2
    print(get_weather('beijing'))

    exit()




    # 测试1
    data = [[0,4,'设备名称：设备1 <br> 资产编号：ABC123'],[3,3,1],[2,6,1],[5,7,1],[0,8,1],[15,9,2]]
    data1 = [[0,0,'设备名称：设备1 <br> 资产编号：ABC123'],[0,1,'设备2'],[0,2,'设备3'],[0,23,'设备4']]
    data2 = [[1,1,'设备名称：设备1 <br> 资产编号：ABC123'],[3,2,20],[6,3,20]]
    data3 = [[12,19,'设备名称：设备1 <br> 资产编号：ABC123'],[12,22,20],[12,23,20]]

    input_data = [{"value":"0", "name":"aaa", "device_code": "ABC001"},
                  {"value":"1", "name":"bbb", "device_code": "ABC002"},
                  {"value":"1", "name":"ccc", "device_code": "ABC002"},
                  {"value":"1", "name":"ddd", "device_code": "ABC002"},
                  {"value":"1", "name":"eee", "device_code": "ABC002"},
                  {"value":"2", "name":"fff", "device_code": "ABC002"},
                  {"value":"2", "name":"ggg", "device_code": "ABC002"},
                  {"value":"3", "name":"hhh", "device_code": "ABC003"}]
    import config
    # for i in get_device_monitor_data(input_data):
    for i in get_device_monitor_data(config.device_monitor_data[:100]):
        print(i)
