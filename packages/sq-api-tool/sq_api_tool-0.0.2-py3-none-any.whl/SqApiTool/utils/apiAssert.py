from .handle_loguru import log

class ApiAssert:
    @classmethod #静态方法
    def api_assert(cls,result,condition,exp_result):
        pass_msg = '验证通过,断言结果:预期结果:{0},实际结果:{1}'  # 通过的断言日志信息
        fail_msg = '验证失败,断言结果:预期结果:{0},实际结果:{1}'  # 失败的断言日志信息
        try:
            assert_type = {
                '==':result == exp_result ,
                '!=':result != exp_result,
                ">":result > exp_result if not isinstance(exp_result,list) else False,
                '<':result < exp_result if not isinstance(exp_result,list) else False,
                'in':result in exp_result if  isinstance(exp_result,list) else False,
                'not in': result not in  exp_result if  isinstance(exp_result,list) else False
            }
            #使用断言类型
            if condition in assert_type: #断言存在
                assert assert_type[condition]
            else:
                raise AssertionError('请输入正确的断言情况')
            log.info(
                f'断言情况{condition}:{pass_msg.format(exp_result, result)}')  # 写日志{msg描述}，断言情况{condition}，成功日志信息
        except Exception as error:
            log.info(
                f'断言情况{condition}:{fail_msg.format(exp_result, result)}')  # 写日志{msg描述}，断言情况{condition},失败日志信息
            log.error(error)
            raise error




if __name__ == '__main__':
    #print(11 if 5>2 else True)  #满足if返回if前面   不满足返回else
    # dict1={'code':0}
    # dict2 = {'code':0}
    ApiAssert.api_assert(5,'iasdasdn',[1,2,3,4])
