import requests
from .utils.handle_loguru import log
import traceback


class Exec:
    token = None
    def __init__(self,data):
        self.data = data
        if Exec.token and isinstance(self.data['请求头'],dict):
            self.data['请求头']['X-AUTH-TOKEN'] = Exec.token

    def request_send(self):
        try:
            if self.data['请求类型'] == {"Content-Type":"application/json"}:
                if self.data['请求头'] != '无':
                    resp = requests.request(method=self.data['请求方式'],url=self.data['URL'],json=self.data['请求参数'],headers=self.data['请求头'])
                    log.info(f'''接口名称：{self.data["接口名称"]},模块名称:{self.data["模块"]}''')
                    log.info(f'响应状态码:{resp.status_code}')
                    log.info(f'请求url:{resp.request.url}')
                    log.info(f'请求头:{resp.request.headers}')
                    log.info(f'请求体:{resp.request.body}')
                    log.info(f'响应头：{resp.headers}')
                    log.info(f'响应体:{resp.json()}')
                else:
                    resp = requests.request(method=self.data['请求方式'],url=self.data['URL'],json=self.data['请求参数'])
                    log.info(f'''接口名称：{self.data["接口名称"]},模块名称:{self.data["模块"]}''')
                    log.info(f'响应状态码:{resp.status_code}')
                    log.info(f'请求url:{resp.request.url}')
                    log.info(f'请求头:{resp.request.headers}')
                    log.info(f'请求体:{resp.request.body}')
                    log.info(f'响应头：{resp.headers}')
                    log.info(f'响应体:{resp.json()}')
                if resp.json().get('token'):
                    Exec.token = resp.json()['token']
                return resp.json()
        except Exception:
            log.error(traceback.format_exc())

