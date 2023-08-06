# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 16:42:21
# @Author  : Pane Li
# @File    : network_services.py
"""
network_services

"""
import allure
from inhandtest.tools import loop_inspector

from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators


class Dhcp(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置Dhcp')
    def config_dhcp(self, **kwargs):
        """

        :param kwargs:
               dhcp_server:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'Gigabitethernet 0/110.5.24.97')]
                [('add', {'enable_dhcp_server': 'enable', 'interface': 'Gigabitethernet 0/1',
                         'start_address': '192.168.2.2', 'end_address': '192.168.2.234', 'lease': 1440})]
                   add parameters:
                        enable_dhcp_server: 'enable', 'disable'
                        interface: 'Gigabitethernet 0/1', 'Cellular 1',
                        start_address:
                        end_address:
                        lease: 30-10080
                        error_text: str or list
                        cancel: True, False
                [('add', {'enable_dhcp_server': 'enable', 'interface': 'Gigabitethernet 0/1',
                         'start_address': '192.168.2.2', 'end_address': '192.168.2.234', 'lease': 1440, 'is_exists': 'Gigabitethernet 0/110.5.24.97'})] 如果存在则不添加
                [('edit', 'Gigabitethernet 0/110.5.24.97', {'enable_dhcp_server': 'enable'})]
                多个操作时使用列表 [('add',{}), ('add',{})]
               windows_name_server: www.baidu.com ex: windows_name_server='www.baidu.com'
               static_ip_setting:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '00:00:00:00:00:0010.5.24.97')]
                [('add', {'mac_address': '00:00:00:00:00:00', 'ip_address': '10.5.24.97'})]
                    add parameters:
                        mac_address: 00:00:00:00:00:00
                        ip_address:
                        error_text: str or list
                        cancel: True, False
                [('add', {'mac_address': '00:00:00:00:00:00', 'ip_address': '10.5.24.97', 'is_exists': '00:00:00:00:00:00'})] 如果存在则不添加
                [('edit', '00:00:00:00:00:00', {'mac_address': '00:00:00:00:00:01'})]
               submit: True,False ex: submit=True
               errors_text: 'ip_address_conflict' ex: errors_text='ip_address_conflict'
               success_tip: True,False ex: success_tip=True
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_services.dhcp')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.dhcp_locators, kwargs)


class Dns(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置Dns')
    def config_dns(self, **kwargs):
        """

        :param kwargs:
               primary_dns: 8.8.8.8 ex: primary_dns='8.8.8.8'
               secondary_dns: 114.114.114.114 ex: secondary_dns='114.114.114.114'
               submit_dns_server: True,False ex: submit_dns_server=True
               enable_dns_relay: enable,disable ex: enable_dns_relay='enable'
               domain_ip_address_pair:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'ss.dc.com10.5.24.97')]
                [('add', {'host': 'ss.dc.com', 'ip_address1': '10.5.24.97', 'ip_address2': '10.5.24.98'})]
                    add parameters:
                        host: ss.dc.com
                        ip_address1:
                        ip_address2:
                        error_text: str or list
                        cancel: True, False
                [('add', {'host': 'ss.dc.com', 'ip_address1': '10.5.24.97', 'ip_address2': '10.5.24.98', 'is_exists': 'ss.dc.com10.5.24.97'})] 如果存在则不添加
                [('edit', 'ss.dc.com10.5.24.97', {'host': 'ss.db.com'})]
               submit_domain_ip_address_pair: True,False ex: submit=True
               errors_text: 'ip_address_conflict' ex: errors_text='ip_address_conflict'
               success_tip: True,False ex: success_tip=True
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_services.dns')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.dns_locators, kwargs)


class Gps(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言GPS状态')
    @loop_inspector('gps_status')
    def assert_gps_status(self, **kwargs):
        """
        :param kwargs:
               gps_status: enable,disable, ex: gps_status='"${value}"=="enable"'
               time_: 0 day 00:00:00 ex: time_='"${value}".startswith("0 day 00:00")'
               location: 成都市 ex: location='"${value}".startswith("成都市")'
               speed:

        """
        self.access_menu('network.network_services.gps.gps configure')
        return self.eval_locator_attribute(kwargs, self.network_locators.gps_status_locators)

    @allure.step('获取GPS状态')
    def get_gps_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               gps_status, time_, location, speed
        """
        self.access_menu('network.network_services.gps.gps configure')
        return self.get_text(keys, self.network_locators.gps_status_locators)

    @allure.step('配置GPS')
    def config_gps(self, enable=True, success_tip=False):
        """

        :param enable: True,False ex: enable=True
        :param success_tip: True,False ex: success_tip=True
        :return:
        """
        self.access_menu('network.network_services.gps.gps configure')
        if success_tip:
            self.agg_in(self.network_locators.gps_locators, {'enable': enable, 'success_tip': 'submit_success'})
        else:
            self.agg_in(self.network_locators.gps_locators, {'enable': enable})

    @allure.step('配置GPS IP Forwarding')
    def config_gps_ip_forwarding(self, **kwargs):
        """ 需要注意的是，在不同的模式下，只有部分参数可用

        :param kwargs:
               enable: True,False ex: enable=True
               type_: client,server ex: type_='client'
               transmit_protocol: UDP,TCP ex: transmit_protocol='UDP'
               connection_type: long_lived,short_lived ex: connection_type='long_lived'
               keepalive_interval: 30 ex: keepalive_interval=30
               keepalive_retry: 3 ex: keepalive_retry=3
               idle_timeout: 60 ex: idle_timeout=60
               local_port: 10000 ex: local_port=10000
               min_reconnect_interval: 60 ex: min_reconnect_interval=60
               max_reconnect_interval: 300 ex: max_reconnect_interval=300
               source_interface: Cellular 1,Dot11radio 1,Gigabitethernet 0/1,Gigabitethernet 0/2, Openvpn 1, Bridge 1 ex: source_interface='Cellular 1'
               reporting_interval: 60 ex: reporting_interval=60
               include_rmc: enable,disable ex: include_rmc='enable'
               include_gsa: enable,disable ex: include_gsa='enable'
               include_gga: enable,disable ex: include_gga='enable'
               include_gsv: enable,disable ex: include_gsv='enable'
               message_prefix: prefix, ex: message_prefix='prefix'
               message_suffix: suffix, ex: message_suffix='suffix'
               destination_ip_address:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'ss.dc.com10.5.24.97')]
                [('add', {'server': 'ss.dc.com', 'port': 10000})]
                    add parameter:
                        server:
                        port:
                        errors_text: str or list
                        cancel: True, False
                [('add', {'server': 'ss.dc.com', 'port': 10000, 'is_exists': 'ss.dc.com10000'})] 如果存在则不添加
                [('edit', 'ss.dc.com10000', {'server': 'ss.db.com'})]
               submit: True,False ex: submit=True
               errors_text: 'ip_address_conflict' ex: errors_text='ip_address_conflict'
               success_tip: True,False ex: success_tip=True
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_services.gps.gps ip forwarding')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.gps_ip_forwarding_locators, kwargs)

    @allure.step('配置GPS Serial Forwarding')
    def config_gps_serial_forwarding(self, **kwargs):
        """ 需要注意的是，在不同的模式下，只有部分参数可用

        :param kwargs:
               enable: True,False ex: enable=True
               serial_type: RS232,RS485,server ex: type_='client'
               baudrate: 9600,19200,38400,57600,115200 ex: baudrate=9600
               data_bits: 7,8 ex: data_bits=5
               parity: none,odd,even ex: parity='none'
               stop_bit: 1,2 ex: stop_bits=1
               software_flow_control: enable,disable ex: software_flow_control='enable'
               include_rmc: enable,disable ex: include_rmc='enable'
               include_gsa: enable,disable ex: include_gsa='enable'
               include_gga: enable,disable ex: include_gga='enable'
               include_gsv: enable,disable ex: include_gsv='enable'
               submit: True,False ex: submit=True
               errors_text: 'ip_address_conflict' ex: errors_text='ip_address_conflict'
               success_tip: True,False ex: success_tip=True
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_services.gps.gps serial forwarding')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.gps_serial_forwarding_locators, kwargs)


class HostList(BasePage, IgLocators):
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言HostList状态')
    @loop_inspector('host_list_status')
    def assert_hostlist_status(self, **kwargs):
        """
        :param kwargs:
               interface: Gigabitethernet 0/1,Gigabitethernet 0/2, ex: interface='Gigabitethernet 0/1'
               mac_address: 00:00:00:00:00:00 ex: mac_address='00:00:00:00:00:00'
               ip_address: 1.1.1.1 ex: ip_address='1.1.1.1'
               host: host1 ex: host='host1'
               exist: True,False ex: exist=True # True:存在,False:不存在， 默认查询存在
        """
        if kwargs:
            self.access_menu('network.network_services.host_list')
            exist = True if kwargs.get('exist') is None else kwargs.pop('exist')
            value = ''
            for cl_ in ('interface', 'mac_address', 'ip_address', 'host'):
                if kwargs.get(cl_):
                    value = value + kwargs.get(cl_)
                else:
                    value = value + '.*'
            if exist:
                return self.table_tr(self.network_locators.hostlist_status_locators, [('exist', value)], 'host list')[0]
            else:
                return not \
                    self.table_tr(self.network_locators.hostlist_status_locators, [('exist', value)], 'host list')[0]
        else:
            return True
