# -*- coding: utf-8 -*-
"""
20210602 zhongs
1 pyproj建议使用2.6.1
2 高德地理逆变码进行调整
"""

import math
import requests
import pyproj
import numpy as np

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False


def gcj02tobd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度

    :return: bd_lng:百度坐标系经度
    :return: bd_lat:百度坐标系纬度
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return bd_lng, bd_lat


def wgs84togcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    #    if out_of_china(lng, lat):  # 判断是否在国内
    #        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return mglng, mglat


def wgs84tobd09(lng, lat):
    '''
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    '''
    lng_gcj, lat_gcj = wgs84togcj02(lng, lat)
    lng_bd, lat_bd = gcj02tobd09(lng_gcj, lat_gcj)

    return lng_bd, lat_bd


def bd09togcj02(bd_lon, bd_lat):
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return gg_lng, gg_lat


def gcj02towgs84(lng, lat):
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat


def wgs84toaddress(lng, lat):
    lng_bd, lat_bd = wgs84tobd09(lng, lat)
    url = 'http://api.map.baidu.com/geocoder?output=json&key=f247cdb592eb43ebac6ccd27f796e2d2&location=' + str(
        lat_bd) + ',' + str(lng_bd)
    print(url)
    response = requests.get(url)
    answer = response.json()
    result = answer['result']
    print(result)
    district = result['formatted_address']
    return district


def wgs84toaddress2(lng, lat):
    lng_bd, lat_bd = wgs84tobd09(lng, lat)
    url = 'http://api.map.baidu.com/geocoder/v2/?&location=%s,%s&output=json&pois=1&ak=awHAux9onnXI2G8kMX7u4wnCREnT1NDz' % (
    lat_bd, lng_bd)

    try:
        response = requests.get(url)

        answer = response.json()
        # print(answer)
        result = answer['result']
        # print(result)
        district = result['formatted_address']
        location = result['sematic_description']
        # print('formatted_address', district)
        # print('sematic_description', location)
        return district, location
    except Exception as e:
        print(e)
        return 'queryErr', 'queryErr'


def wgs84toutm(lng, lat):
    '''
    WGS84转大地坐标系
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    '''
    zone = int(lng // 6) + 31
    p = pyproj.Proj(proj='utm', zone=zone, ellps='WGS84')  # (lon+180)/6
    x, y = p(lng, lat)
    return x, y


def utmtowgs84(x, y, p):
    # utm x y 转成lnglat
    # p: 坐标转换关系，包含经纬度所属区域
    # return: wgs84坐标系 lng lat
    lng, lat = p(x, y, inverse=True)
    return round(lng, 8), round(lat, 8)


def gcjtoutm(lng, lat):
    # 高德转大地坐标系
    lng, lat = gcj02towgs84(lng, lat)
    zone = int(lng // 6) + 31
    p = pyproj.Proj(proj='utm', zone=zone, ellps='WGS84')  # (lon+180)/6
    x, y = p(lng, lat)
    return x, y


def xy_interpolation(x1, x2, l1, l2):
    # 对x1、x2的中间点进行插值
    # x1、x2为两端的位置
    # l1、l2为中间点到两端的距离
    # print('', l1, l2, l1+l2)
    return (l1 * x2 + l2 * x1) / (l1 + l2)


def lnglat_interpolation(lng1, lat1, lng2, lat2, l1, l2):
    # 对两个经纬度的中间点坐标进行插值
    # l1、 l2为桩号差
    zone = int(round((lng1 / 6 + 30), 0))
    p = pyproj.Proj(proj='utm', zone=zone, ellps='WGS84')
    x1, y1 = p(lng1, lat1)
    x2, y2 = p(lng2, lat2)

    x0 = xy_interpolation(x1, x2, l1, l2)
    y0 = xy_interpolation(y1, y2, l1, l2)

    lng0, lat0 = utmtowgs84(x0, y0, p)
    return lng0, lat0


###############################################################################
# 数字转桩号
def stakeNum_to_stakeInfo(i_stakeNum):
    return "K%d+%d" % (i_stakeNum / 1000, i_stakeNum % 1000)


def return_distance(lng1, lat1, lng2, lat2):
    '''
    利用wgs84坐标计算两个点的距离
    :param lng1: 点A wgs84经度
    :param lat1: 点A wgs84纬度
    :param lng2: 点B wgs84经度
    :param lat2: 点B wgs84纬度
    :return: 距离(m)
    '''
    zone = int(lng1 // 6) + 31
    p = pyproj.Proj(proj='utm', zone=zone, ellps='WGS84')  # 使用同一个p进行处理
    x1, y1 = p(lng1, lat1)
    x2, y2 = p(lng2, lat2)

    vector1 = np.array([x1, y1])
    vector2 = np.array([x2, y2])

    distance = np.linalg.norm(vector1 - vector2)
    return distance


# 计算两点的方向角
def azimuthAngle(x1, y1, x2, y2):
    angle = 0.0
    dx = x2 - x1
    dy = y2 - y1
    if x2 == x1:
        angle = math.pi / 2.0
        if y2 == y1:
            angle = 0.0
        elif y2 < y1:
            angle = 3.0 * math.pi / 2.0
    elif x2 > x1 and y2 > y1:
        angle = math.atan(dx / dy)
    elif x2 > x1 and y2 < y1:
        angle = math.pi / 2 + math.atan(-dy / dx)
    elif x2 < x1 and y2 < y1:
        angle = math.pi + math.atan(dx / dy)
    elif x2 < x1 and y2 > y1:
        angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
    return (angle * 180 / math.pi)


# 高德地理坐标逆编码，进行调整
def gcjtoaddress(lng, lat):
    '''
    gcj坐标地理逆编码,空信息以'[]'的形式返回,错误返回-1
    :param lng: gcj坐标系经度
    :param lat: gcj坐标系纬度
    :return: 省,市/区,街道,路,格式化地址,最近的路口信息
    '''
    url = f'https://restapi.amap.com/v3/geocode/regeo?output=json&location={lng},{lat}&key=383048874d6e9c4d63041b17830701a1&radius=2000&extensions=all'
    # print(url)
    response = requests.get(url)
    answer = response.json()

    # 提取有效信息
    result = answer['regeocode']

    # 获取所在道路信息
    loc_area = str(result['addressComponent']['province']) + str(result['addressComponent']['city']) + str(
        result['addressComponent']['district'])
    loc_area = loc_area.replace("[]", "")  # 去除列表符号

    try:
        if float(result['roads'][0]['distance']) > 25:  # 如果该点位与最近的道路距离超过25米，则认为该点位不在路上
            loc_road = result['formatted_address']  # 点位在小区或者靠近某个设施
        else:  # 如果相差不到25米，认为该点位在路上
            loc_road = loc_area + result['roads'][0]['name']
    except Exception as e:  # 如果该区域没有路段，则直接使用逆变码地址
        loc_road = result['formatted_address']  # 点位在小区或者靠近某个设施

    # 获取交叉口信息
    try:
        location_first_name = result['roadinters'][0]['first_name']
        location_second_name = result['roadinters'][0]['second_name']
        location_direction = result['roadinters'][0]['direction']
        location_distance = result['roadinters'][0]['distance']
        loc_location = f"{location_first_name}与{location_second_name}交叉口{location_direction}{location_distance}米"
    except Exception as e:
        print("请求链接出错", e)
        loc_location = ''
    return loc_road, loc_location


def road_gps_point_from_bd09(lng_bd1, lat_bd1, lng_bd2, lat_bd2, ak="cjG6Oji1O7Mb4mGomaNlzxbS1qiV02Pm",
                             method='driving'):
    '''
    输入起终点经纬度
    输出路线途经点的经纬度
    method 默认为driving，可以选择riding
        driving: 对应驾车
        riding:  对应自行车
    '''
    url = "http://api.map.baidu.com/direction/v2/{}?origin={},{}&destination={},{}&ak={}".format(method, lat_bd1,
                                                                                                 lng_bd1, lat_bd2,
                                                                                                 lng_bd2, ak)
    response = requests.get(url)
    answer = response.json()
    result = answer['result']
    routes = result["routes"]
    steps = routes[0]['steps']
    lnglat_select = []
    last_lnglat = ''
    for i, i_step in enumerate(steps):

        i_path = i_step['path']
        i_lnglat_list = i_path.split(";")
        for j, j_lnglat in enumerate(i_lnglat_list):
            if last_lnglat == j_lnglat:  # 如果是重复的经纬度，不进行计入
                continue

            lnglat_select.append(j_lnglat)
            last_lnglat = j_lnglat
    # print(answer)

    return lnglat_select


def road_gps_point_from_gcj(lng_gcj1, lat_gcj1, lng_gcj2, lat_gcj2, ak="cjG6Oji1O7Mb4mGomaNlzxbS1qiV02Pm",
                            method='driving'):
    ''' 调用百度api
    输入起终点经纬度
    输出路线途经点的经纬度
    '''
    lng_bd1, lat_bd1 = gcj02tobd09(lng_gcj1, lat_gcj1)
    lng_bd2, lat_bd2 = gcj02tobd09(lng_gcj2, lat_gcj2)
    lnglat_select = road_gps_point_from_bd09(lng_bd1, lat_bd1, lng_bd2, lat_bd2, ak, method)

    return lnglat_select


def pts_dist_xy(x1, y1, x2, y2):
    '''
    计算两点间距(xy)
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    '''
    return round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2), 3)


def pts_dist_lnglat(lng1, lat1, lng2, lat2):
    '''
    计算两点间距(经纬度)
    :param lng1: 第一个点的经度
    :param lat1: 第一个点的纬度
    :param lng2: 第二个点的经度
    :param lat2: 第二个点的纬度
    :return:     返回两点间距(单位m)
    '''
    x1, y1 = wgs84toutm(lng1, lat1)
    x2, y2 = wgs84toutm(lng2, lat2)
    return pts_dist_xy(x1, y1, x2, y2)


if __name__ == "__main__":
    # import pandas as pd
    # data=pd.read_excel(r"D:\项目数据\2021年项目数据\20210421_徐汇井盖\2021-11月徐汇井盖\2021-11-徐汇问题井盖_v3.xlsx",sheet_name="问题井盖")
    # data[["loc_area","loc_location"]]=data.apply(lambda row:gcjtoaddress(row["longitude_gcj"],row["latitude_gcj"]),axis=1,result_type="expand")
    # data.to_excel(r"D:\项目数据\2021年项目数据\20210421_徐汇井盖\2021-11月徐汇井盖\2021-11-徐汇问题井盖_v4.xlsx",index=None)
    # print(gcjtoaddress(113.9158541507666,21.997084380976084))
    print(gcj02towgs84(121.111362566, 31.164911318))
