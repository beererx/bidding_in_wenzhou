from flask import Flask, jsonify, request
import json
from settings import REQUEST_LISTS, TITLES
import re
import rsa
import base64
import time
import random
from mysql_con import Bidding

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

# 检查是否含有特殊字符
def is_string_validate(str):
    sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",str)
    if len(str) == len(sub_str):
        # 合法
        return False
    else:
        # 不合法
        return True

@app.route('/', methods=['GET'])
def hell_world():
    bidding = Bidding()
    sql_data = bidding.get_all()
    resData = {
        "resCode": 0,
        "data": sql_data,
        "message": '首页信息'
    }
    return jsonify(resData)

@app.route('/', methods=['POST'])
def get_all_infos():
    get_data = json.loads(request.get_data(as_text=True))
    city = get_data['key'][0]
    content = get_data['key'][1]
    bidding = Bidding()
    sql_data = bidding.get_appoint(city, content)
    resData = {
        "resCode": 0,
        "data": sql_data,
        "message": '搜索信息'
    }
    return jsonify(resData)

@app.route('/content/<noteid>', methods=['POST'])
def get_sep_infos(noteid):
    get_data = json.loads(request.get_data(as_text=True))
    bidding = Bidding()
    sql_data = bidding.get_content(noteid)
    resData = {
        "resCode": 0,
        "data": sql_data,
        "message": '搜索信息'
    }
    return jsonify(resData)

@app.route('/content/<dt>/<noteid>', methods=['POST'])
def get_sep_infos2(dt,noteid):
    get_data = json.loads(request.get_data(as_text=True))
    bidding = Bidding()
    sql_data = bidding.get_content2(dt, noteid)
    resData = {
        "resCode": 0,
        "data": sql_data,
        "message": '搜索信息'
    }
    return jsonify(resData)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8088, debug=True)


