import os
import pytest
import allure
from .utils.handle_excel import get_excel_data
from Exec import Exec
from .utils.apiAssert import ApiAssert
import sys

filepath = sys.argv[1]
project = filepath.split('\\')[-1].split('.')[0]


@pytest.mark.parametrize('data',get_excel_data(filepath))
@allure.epic(f'{project}')
def test_tmp(data):
    allure.dynamic.feature(data["模块"])
    allure.dynamic.title(data["用例编号"]+data["标题"])
    res = Exec(data).request_send()
    ApiAssert.api_assert(res['code'],'==',data['预期结果']['code'])


if __name__ == '__main__':
    pytest.main([__file__,'-s','--alluredir','report/tmp'])
    os.system('allure serve report/tmp')
