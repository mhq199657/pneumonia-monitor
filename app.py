from time import sleep
from datetime import datetime
from urllib import request

webpath = "https://3g.dxy.cn/newh5/view/pneumonia"
provinces = ["北京市","天津市","上海市","重庆市","河北省","山西省",\
"辽宁省","吉林省","黑龙江省","江苏省","浙江省","安徽省","福建省","江西省",\
"山东省","河南省","湖北省","湖南省","广东省","海南省","四川省","贵州省",\
"云南省","陕西省","甘肃省","青海省","台湾省","内蒙古自治区","广西壮族自治区",\
"西藏自治区","宁夏回族自治区","新疆维吾尔自治区","香港特别行政区","澳门特别行政区"]
CONFIRMED_STRING = "确诊"
PENDING_STRING = "疑似"
LI_STRING = "例"

class WebsiteUpdate:
  def __init__(self):
    self.confirmedCounts = {}
    self.pendingCounts = {}
    self.updateTimestamp = datetime.now()
    for province in provinces:
      self.confirmedCounts[province] = 0
      self.pendingCounts[province] = 0
  def __str__(self):
    ret = ""
    ret += "Province\tConfirmed\tPending\n"
    for province in provinces:
      ret += province + "\t" + str(self.confirmedCounts[province]) + "\t" + str(self.pendingCounts[province]) + "\n"
    ret += "Last update: " + self.updateTimestamp.strftime("%Y-%m-%d %H:%M:%S")
    return ret
    

class App:
  def __init__(self, refresh_time = 10):
    self.refresh_time_ = refresh_time
    self.updates = []
  def update(self):
    print("Alive")
  def run(self):
    while True:
      source = self.getResponse()
      code, update = self.parseResponse(source)
      if code == -1:
        continue
      self.compareAgainstHistory(update)
      self.updates.append(update)
      sleep(10)
    
  def getResponse(self):
    responses = request.urlopen(webpath).readlines()
    source = b''
    for response in responses:
      source += response

    return source.decode("utf-8")

  def parseResponse(self,source):
    # print(source)
    try:
      data_eval = "[" + source.split("window.getListByCountryTypeService1 = ")[1].split("[")[1].split("]")[0] + "]"
      data = eval(data_eval)
    except:
      print("Error getting website")
      return -1, None
    update = WebsiteUpdate()
    def parseConfirmedAndPending(info):
      confirmedCount = 0
      pendingCount = 0
      if CONFIRMED_STRING in info:
        confirmedCount = int(info.split(CONFIRMED_STRING)[1].split(LI_STRING)[0].strip(" "))
      if PENDING_STRING in info:
        try:
          pendingCount = int(info.split(PENDING_STRING)[1].split(LI_STRING)[0].strip(" "))
        except:
          pass
      return confirmedCount, pendingCount
    for item in data:
      confirmedCount, pendingCount = parseConfirmedAndPending(item["tags"])
      provinceName = item["provinceName"]
      update.confirmedCounts[provinceName] = confirmedCount
      update.pendingCounts[provinceName] = pendingCount
    return 0, update

  def compareAgainstHistory(self,update):
    if len(self.updates) == 0:
      print("This is the first update so far")
    else:
      last = self.updates[-1]
      diff = WebsiteUpdate()
      for province in provinces:
        print(update.confirmedCounts[province])
        print(last.confirmedCounts[province])
        confirmedIncrement = update.confirmedCounts[province] - last.confirmedCounts[province]
        if confirmedIncrement != 0:
          diff.confirmedCounts[province] = confirmedIncrement
        pendingIncrement = update.pendingCounts[province] - last.pendingCounts[province]
        if pendingIncrement != 0:
          diff.pendingCounts[province] = pendingIncrement
      print(diff)
        
        


      

