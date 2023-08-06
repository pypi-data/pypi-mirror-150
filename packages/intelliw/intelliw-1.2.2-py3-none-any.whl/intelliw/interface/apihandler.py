'''
Author: hexu
Date: 2021-10-25 15:20:34
LastEditTime: 2022-05-16 15:55:27
LastEditors: Hexu
Description: api处理函数
FilePath: /iw-algo-fx/intelliw/interface/apihandler.py
'''
import sys
import time
import json
import traceback
import tornado
from tornado import web
from tornado.options import options
import intelliw.utils.message as message
from intelliw.config import config
from intelliw.utils.util import default_dump
from intelliw.utils.global_val import gl
from urllib.parse import parse_qs
from intelliw.utils.logger import get_logger

logger = get_logger()

class BaseHandler(web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

    # json
    def get_json_argument(self):
        rawreqinfos = self.request.body.decode('utf-8')
        if not rawreqinfos:
            return {}
        data = json.loads(rawreqinfos)
        return data if isinstance(data, dict) else {"data":data}

    # form
    def get_form_argument(self):
        rawreqinfos = self.request.body.decode('utf-8')
        if not rawreqinfos:
            return {}
        return parse_qs(rawreqinfos)
    
    # request
    def request_process(self):
        req_data = dict()
        ok = True
        try:
            # query 
            req_data = {key: eval(self.get_argument(key)) for key in self.request.query_arguments.keys()}
            
            # body
            content_type = self.request.headers.get('Content-Type', "").strip()
            if content_type.startswith('application/x-www-form-urlencoded'):
                req_data.update(self.get_form_argument())
            elif content_type.startswith('application/json'):
                req_data.update(self.get_json_argument())
            elif content_type.startswith('multipart/form-data'):
                req_data.update({key: eval(self.get_argument(key)) if self.get_argument(key) else self.get_argument(key) for key in self.request.body_arguments.keys()})
            # files 
            if self.request.files:
                req_data["files"] = list()
                for files in self.request.files.values():
                    req_data["files"].extend(files)
        except Exception as e:
            req_data = str(message.APIResponse(400, "api", f"API服务请求解析错误: {e}, Body: {str(self.request.body)}"))
            return req_data, not ok
        return req_data, ok
    
    # response
    def response_process(self, data):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        try:
            result, emsg = options.infer.infer(data, self.func, self.need_featrue)
            if emsg is None:
                resp = str(message.APIResponse(200, "api", '', result))
            else:
                resp = str(message.APIResponse(500, "api", emsg, result))
        except Exception as e:
            self.error_report(e)
            resp = str(str(message.APIResponse(
                500, "api", "API服务处理推理数据错误 {}".format(e))))
        return resp

    # error report
    def error_report(self, e: Exception):
        stack_info = traceback.format_exc()
        logger.error("API服务处理推理数据错误 {} stack: {}".format(e, stack_info))
        msg = [{'status': 'inferfalied',  'inferid': config.INFER_ID, 'instanceid': config.INSTANCE_ID,
                'inferTaskStatus': [{
                    "id": config.INFER_ID, "issuccess": False,
                    "starttime": int(time.time() * 1000),
                    "endtime": int(time.time() * 1000),
                    "message": "API服务处理推理数据错误"
                }]}]
        self.application.reporter.report(message.CommonResponse(500, "inferstatus", "API服务处理推理数据错误 {}".format(
            e), json.dumps(msg, default=default_dump, ensure_ascii=False)))

    # error method
    def error_method(self, func_method):
        if self.method != func_method:
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            self.write(str(message.APIResponse(
                500, "api", "请求方法({}) 与配置方法({}) 不一致，如果未设置method，默认为post".format(func_method, self.method))))
            return "err"
        return None
    

class HealthCheckHandler(BaseHandler):
    """健康检查"""

    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(str(message.HealthCheckResponse(200, "api", 'ok', "")))

    def get(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(str(message.HealthCheckResponse(200, "api", 'ok', "")))


class MainHandler(BaseHandler):
    def initialize(self, func, method='post', need_featrue=True):
        self.func = func
        self.method = method
        self.need_featrue = need_featrue
    
    def get(self):
        self.__do(sys._getframe().f_code.co_name)

    def post(self):
        self.__do(sys._getframe().f_code.co_name)
    
    def put(self):
        self.__do(sys._getframe().f_code.co_name)
    
    def delete(self):
        self.__do(sys._getframe().f_code.co_name)
   
    def options(self):
        self.__do(sys._getframe().f_code.co_name)
    
    def patch(self):
        self.__do(sys._getframe().f_code.co_name)
    
    def head(self):
        self.__do(sys._getframe().f_code.co_name)

    def __do(self, method):
        if not self.error_method(method):
            result, ok = self.request_process()
            if ok:
                result = self.response_process(result)
            self.write(result)
