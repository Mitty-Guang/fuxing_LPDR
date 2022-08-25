import datetime
import math
from cities import cities, provinceurl, cityurl

def getProvince(str):
    province = cities.get(str[0])
    return province

def getCity(str):
    city = cities.get(str[:2])
    return city

def getProvinceUrl(str):
    pUrl = provinceurl.get(str)
    return pUrl

def getCityUrl(str):
    cUrl = cityurl.get(str)
    return cUrl

def getModel(lp):
    if len(lp)==7:
        return "传统能源"
    else:
        return "新能源"

def getDuration(strDate1, strDate2):
    if strDate2 == '':
        date2 = datetime.datetime.now()
    else:
        date2 = datetime.datetime.strptime(strDate2, "%Y-%m-%d %H:%M:%S")
    date1 = datetime.datetime.strptime(strDate1, "%Y-%m-%d %H:%M:%S")
    durationDate = date2 - date1
    days = durationDate.days
    totalseconds = durationDate.seconds
    hours = math.floor(totalseconds / (60 * 60))
    minutes = math.floor((totalseconds - hours * 3600) / 60)
    seconds = math.floor(totalseconds - hours * 3600 - minutes * 60)
    duration = str(days) + '天 ' + str(hours) + '时 ' + str(minutes) + '分 ' + str(seconds) + '秒'

    return duration

# print(getModel('皖H123456'))