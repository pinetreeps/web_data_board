# _*_ coding:utf-8 _*_
# Filename: utils.py
# Author: pang song
# python 3.6
# Date: 2018/10/12


def get_device_monitor_data(input_data):
    xx = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9',
          'x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9']
    yy = ['y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9',
          'y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9',
          'y0', 'y1', 'y2', 'y3']
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
                u'设备名称：' + input_data[num_device].get('name') + u'<br> 资产编号：' + input_data[num_device].get('device_code'))
            if input_data[num_device].get('value') == "0":
                device_running_list.append(device)
            elif input_data[num_device].get('value') == "1":
                device_standby_list.append(device)
            elif input_data[num_device].get('value') == "2":
                device_shutdown_list.append(device)
            elif input_data[num_device].get('value') == "3":
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




if __name__ == '__main__':

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
