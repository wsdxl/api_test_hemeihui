from common.contans import DataDir
import os
from common.hander_data import replace_param, replace_data
from common.read_excel import ReadExcel
from common.hande_db import HandDB
from common.login import Login
from common.read_conf import conf
from common.hander_request import HanderRequest


def paramter_fengzhuagn(data_path, sheet_name):
    excel = ReadExcel(data_path, sheet_name)
    pinglun_data = excel.read_excel()
    db = HandDB()
    datas = []
    # 替换用例data列中json数据里得参数
    for case in pinglun_data:
        # 获取用例中的sql参数语句
        sql_str = case["check_sql"]
        # 判断用例是否有需要替换得参数
        if type(sql_str) == str and sql_str.strip() != "":
            # 从数据库中获取用例需要得具体参数
            param = db.get_one(sql_str)
            # 判断是否有符合条件得测试数据
            if len(param) != 0:
                # 将case 中的动态参数替换成上一步从数据库里撸出来得具体参数
                case['data'] = replace_param(case['data'], param)
            else:
                print("缺少相应得测试数据")
        else:
            datas.append(case)
    return datas


def case_package(case, sid):
    base_url = conf.get('hfjyuan', 'url')
    if '#admin_token#' in case['url']:
        case['url'] = case['url'].replace('#admin_token#', conf.get('admin_hfjyuan', 'admin_token'))
    if '#sid#' in case['url']:
        case['url'] = case['url'].replace('#sid#', sid)
    params = {}
    params["url"] = base_url + case['url']
    params["method"] = case['method']
    case['data'] = replace_data(case['data'])
    data = eval(case['data'])
    params["data"] = data
    headers = eval(case['headers'])
    params["headers"] = headers
    expected = eval(case['expected'])
    params["expected"] = expected
    row = case['case_id'] + 1
    params["row"]=row
    return params