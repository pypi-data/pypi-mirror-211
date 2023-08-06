# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 11:05:50
# @Author  : Pane Li
# @File    : vpn.py
"""
vpn

"""
import allure
from inhandtest.tools import loop_inspector

from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators


class Vpn(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言L2tp Status状态')
    @loop_inspector('l2tp_status')
    def assert_l2tp_status(self, client: dict = None, server: dict = None):
        """
        :param client: 字典，包含以下key
                tunnel_name:
                l2tp_server:
                status: disconnect, connect, disable
                time:
                local_ip_address
                remote_ip_address
                local_session_id
                remote_session_id
                exist: True,False ex: exist=True # True:存在,False:不存在， 默认查询存在
        :param server: 字典，包含以下key
               tunnel_name:
               status: disconnect, connect, disable
               time:
               local_ip_address
               remote_ip_address
               exist: True,False ex: exist=True # True:存在,False:不存在， 默认查询存在
        """
        result = True
        if client or server:
            self.access_menu('network.vpn.l2tp.status')
        if client is not None:
            exist = True if client.get('exist') is None else client.pop('exist')
            value = ''
            for cl_ in ('tunnel_name', 'l2tp_server', 'status', 'time', 'local_ip_address', 'remote_ip_address',
                        'local_session_id', 'remote_session_id'):
                if client.get(cl_):
                    value = value + client.get(cl_)
                else:
                    value = value + '.*'
            if exist:
                result = \
                    self.table_tr(self.network_locators.l2tp_client_status_locators, [('exist', value)],
                                  'routing status')[0]
            else:
                result = not \
                    self.table_tr(self.network_locators.l2tp_client_status_locators, [('exist', value)],
                                  'routing status')[0]
        if server is not None:
            exist = True if server.get('exist') is None else server.pop('exist')
            value = ''
            for cl_ in ('tunnel_name', 'status', 'time', 'local_ip_address', 'remote_ip_address'):
                if server.get(cl_):
                    value = value + server.get(cl_)
                else:
                    value = value + '.*'
            if exist:
                result = \
                    self.table_tr(self.network_locators.l2tp_server_status_locators, [('exist', value)],
                                  'routing status')[0]
            else:
                result = not \
                    self.table_tr(self.network_locators.l2tp_server_status_locators, [('exist', value)],
                                  'routing status')[0]
        return result

    @allure.step('配置L2tp Client')
    def config_l2tp_client(self, **kwargs):
        """ 注意如果是删除，需要先删除关联项，再删除本身，否则多次删除会删除不了

        :param kwargs:
            l2tp_class:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'nameyes')]
                [('add', {'name': 'name', 'auth': 'yes', 'hostname': hostname, 'challenge_secret': challenge_secret})]
                    add parameter:
                        name:
                        auth: yes, no
                        hostname:
                        challenge_secret:
                        errors_text: str or list
                        cancel: True, False
                [('add', {'name': 'name', 'hostname': hostname, 'is_exists': 'nameyes'})] 如果存在则不添加
                [('edit', 'nameyes', {'name': 'name1'})]
                [('associate_delete', 'nameyes')]   # 删除关联项
            pseudowire_class:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'namel2tp_class')]
                [('add', {'name': 'name', 'l2tp_class': l2tp_class, 'source_interface': source_interface, 'data_encapsulation_method': data_encapsulation_method, 'tunnel_management_protocol': tunnel_management_protocol})]'})]
                    add parameter:
                        name:
                        l2tp_class: l2tp_class
                        source_interface: 'Cellular 1', 'Bridge 1'
                        data_encapsulation_method: 'L2TPv2', 'L2TPv3'
                        tunnel_management_protocol: 'L2TPv2', 'NONE', 'L2TPv3'
                        errors_text: str or list
                        cancel: True, False
                [('add', {'name': 'name', 'l2tp_class': l2tp_class, 'is_exists': 'namel2tp_class'})] 如果存在则不添加
                [('edit', 'namel2tp_class', {'name': 'name1'})]
                [('associate_delete', 'namel2tp_class')]   # 删除关联项
            l2tpv2_tunnel:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'id')]
                [('add', {'enable': True, 'id': id, 'l2tp_server': l2tp_server, 'pseudowire_class': pseudowire_class, 'auth_type': auth_type, 'username': username, 'password': password, 'local_ip_address': local_ip_address})]
                    add parameter:
                        enable: True, False
                        id: str or int
                        l2tp_server:
                        pseudowire_class:
                        auth_type: 'AUTO', 'PAP', 'CHAP'
                        username: str
                        password: str
                        local_ip_address: str
                        remote_ip_address: str
                        errors_text: str or list
                        cancel: True, False
                [('add', {'enable': True, 'id': id, 'is_exists': 'id'})] 如果存在则不添加
                [('edit', 'id', {'enable': False})]
                [('associate_delete', 'id')]   # 删除关联项
            l2tpv3_tunnel:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'id')]
                [('add', {'enable': True, 'id': id, 'peer_id': peer_id})]
                    add parameter:
                        enable: True, False
                        id: str or int
                        peer_id:
                        pseudowire_class:
                        protocol: 'IP', 'UDP'
                        source_port: int
                        destination_port: int
                        xconnect_interface: str
                        errors_text: str or list
                        cancel: True, False
                [('add', {'enable': True, 'id': id, 'is_exists': 'id'})] 如果存在则不添加
                [('edit', 'id', {'enable': False})]
                [('associate_delete', 'id')]   # 删除关联项
            l2tpv3_session:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'local_session_id')]
                [('add', {'local_session_id': local_session_id, 'remote_session_id': remote_session_id})]
                    add parameter:
                        local_session_id: str or int
                        remote_session_id: str or int
                        local_tunnel_id:
                        local_session_ip_address:
                        errors_text: str or list
                        cancel: True, False
                [('add', {'local_session_id': local_session_id, 'is_exists': 'local_session_id'})] 如果存在则不添加
                [('edit', 'local_session_id', {'local_session_id': local_session_id})]
                [('associate_delete', 'local_session_id')]   # 删除关联项
            submit: True,False ex: submit=True
            errors_text: str or list
            success_tip: True,False ex: success_tip=True
            reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.vpn.l2tp.l2tp client')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.l2tp_client_locators, kwargs)

    @allure.step('配置L2tp Service')
    def config_l2tp_service(self, **kwargs):
        """

        :param kwargs:
            enable： True,False ex: enable=True
            username: str
            password: str
            auth_type: 'AUTO', 'PAP', 'CHAP'
            local_ip_address: str
            client_start_ip: str
            client_end_ip: str
            link_detection_interval:  int
            max_retries_for_link: int
            enable_mppe: True,False ex: enable_mppe=True
            enable_tunnel_auth: True,False ex: enable_tunnel_auth=True
            export_options: str
            submit: True,False ex: submit=True
            errors_text: str or list
            success_tip: True,False ex: success_tip=True
            reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.vpn.l2tp.l2tp service')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.l2tp_service_locators, kwargs)
