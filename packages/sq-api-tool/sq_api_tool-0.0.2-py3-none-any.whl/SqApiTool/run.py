
import pytest
import os



def test_run():
    pytest.main([os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_template.py'),'-sv', '--alluredir', 'report/tmp'])
    os.system('allure serve report/tmp')

if __name__ == '__main__':
    file='D:\教学资料\代码\pyrf\测试用例.xls'
    print(file.split('\\')[-1].split('.')[0])