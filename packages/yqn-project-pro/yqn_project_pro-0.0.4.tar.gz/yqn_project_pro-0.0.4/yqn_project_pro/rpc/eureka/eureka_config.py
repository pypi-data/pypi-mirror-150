# -*- coding: utf-8 -*-
# @Author: Yu
# @File: eureka_config.py
# @Time: 2021/12/16
# @Desc:
import json

from yqn_project_pro.rpc.eureka import eureka_client
from yqn_project_pro.rpc import RPCConfigBase

DEFAULT_HEADERS = {"Content-Type": "application/json"}

DEFAULT_HEADER = {
    "accessToken": "",
    "viewAll": True,
    "xAppId": "",
    "xBPId": "",
    "xCallerId": "",
    "xClientIp": "",
    "xDeviceId": "",
    "xIsTest": False,
    "xJsFinger": "",
    "xLangCode": "",
    "xOpenId": "",
    "xOpenPlatform": "",
    "xPushToken": "",
    "xSession": "",
    "xSourceAppId": "",
    "xSystemLangCode": "",
    "xTestFlag": "",
    "xToken": "",
    "xTraceId": "",
    "xUserId": 1,
    "xUserName": "运去哪超超管",
}


class Eureka(RPCConfigBase):
    def __init__(self, **kwargs):
        super(Eureka, self).__init__(**kwargs)
        self.eureka_app_name = self.client_config.eureka_app_name
        self.eureka_instance_ip = self.client_config.eureka_instance_ip
        self.eureka_instance_host = self.client_config.eureka_instance_host
        self.eureka_instance_port = self.client_config.eureka_instance_port
        self.eureka_status_page_url = self.client_config.eureka_status_page_url
        self.eureka_health_check_url = self.client_config.eureka_health_check_url
        if self.use_conf_management:
            assert (
                self.server_manager
            ), "use_conf_management need server_manager is not None"
            self.eureka_server = self.server_manager.get_value(
                self.client_config.eureka_server_key
            )
        else:
            self.eureka_server = self.client_config.eureka_server_url
        self.eureka_app_name = self.eureka_app_name.replace("_", "-")

    def init_eureka(self):
        eureka_client.init(
            eureka_server=self.eureka_server,
            app_name=self.eureka_app_name,
            instance_ip=self.eureka_instance_ip,
            instance_host=self.eureka_instance_host,
            instance_port=self.eureka_instance_port,
            status_page_url=self.eureka_status_page_url,
            health_check_url=self.eureka_health_check_url,
        )
        self.connector = eureka_client

    def reload(self):
        pass

    def connect(self, **kwargs):
        self.init_eureka()
        return self.connector

    def close(self, **kwargs):
        pass

    def reconnect(self, **kwargs):
        pass

    def do_service(
        self,
        app_name: str = "",  # 应用名
        service: str = "",  # api
        return_type: str = "json",  # 返回格式
        prefer_ip: bool = False,
        prefer_https: bool = False,
        method: str = "GET",  # 请求方式
        headers: dict = None,  # 请求头，默认为application/json
        model: dict = None,  # 请求子参数model
        header: dict = None,
        timeout: int = 5,
    ):
        data = {
            "header": header if header else DEFAULT_HEADER,
            "model": model,
        }
        headers = dict(DEFAULT_HEADERS, **headers) if headers else DEFAULT_HEADERS
        return self.connector.do_service(
            app_name=app_name,
            service=service,
            return_type=return_type,
            prefer_ip=prefer_ip,
            prefer_https=prefer_https,
            method=method,
            headers=headers,
            data=json.dumps(data, ensure_ascii=False).encode(),
            timeout=timeout,
        )
