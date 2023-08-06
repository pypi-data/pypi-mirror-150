import xlrd
from .handle_md5 import get_md5_data


def get_excel_data(fileDir):
    wookbook = xlrd.open_workbook(fileDir,formatting_info=True)
    sheets = wookbook.sheet_names()
    reslist = [] # [{}]
    for sheet in sheets:
        new_sheet = wookbook.sheet_by_name(sheet)
        for one in range(1,new_sheet.nrows):
            data_dict = dict(zip(new_sheet.row_values(0),new_sheet.row_values(one)))
            data_dict['请求参数'] = eval(data_dict['请求参数'])
            if sheet == '登录模块':
                data_dict['请求参数']['password'] = get_md5_data(data_dict['请求参数']['password'])
            data_dict['请求类型'] = eval(data_dict['请求类型'])
            data_dict['预期结果'] = eval(data_dict['预期结果'])
            if data_dict['请求头'] != '无':
                data_dict['请求头'] = eval(data_dict['请求头'])
            reslist.append(data_dict)
    return reslist




if __name__ == '__main__':
    from pprint import pprint
    pprint(get_excel_data('../考试系统.xls'))