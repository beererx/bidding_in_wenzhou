import requests
import re

url = "http://search.zj.gov.cn/jrobotfront/interfaces/artranklist.do"

param = {
    "websiteid": "330324000000000",
    "up": "1",
}

resp = requests.post(url, params=param)
page_content = resp.text
print(resp.text)

#解析数据
noteid_obj = re.compile(r'/art_(?P<text>.*?).html', re.S)
title_obj = re.compile(r'"title":"(?P<text>.*?)","url":', re.S)
url2_obj = re.compile(r'"url":"(?P<text>.*?)","weight', re.S)
time_obj = re.compile(r'/art/(?P<text>.*?)/art_', re.S)
#开始匹配
noteid = noteid_obj.finditer(page_content)
title = title_obj.finditer(page_content)
url2 = url2_obj.finditer(page_content)
time = time_obj.finditer(page_content)

for it in time:
    print(it.group("text"))

