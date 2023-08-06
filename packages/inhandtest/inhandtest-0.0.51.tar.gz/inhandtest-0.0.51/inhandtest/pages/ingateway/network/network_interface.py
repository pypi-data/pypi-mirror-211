# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 16:22:44
# @Author  : Pane Li
# @File    : network_interface.py
"""
network_interface

"""
import allure
from inhandtest.tools import loop_inspector
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators


class Cellular(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言蜂窝状态')
    @loop_inspector('cellular_status')
    def assert_cellular_status(self, **kwargs):
        """

        :param kwargs:
                     active_sim: SIM 1,SIM 2,sim 1,sim 2 ex: active_sim='"${value}" =="sim 1"'
                     imei: 123456789012345 ex: imei='"${value}" == "123456789012345"'
                     imsi: 123456789012345 ex: imsi='"${value}" == "123456789012345"'
                     iccid: 123456789012345 ex: iccid='"${value}" == "123456789012345"'
                     register_status: not_register,registering,connected,disconnected ex: register_status='"${value}" == "not_register"'
                     operator: China Mobile,China Unicom,China Telecom ex: operator='"${value}" == "China Mobile"'
                     network_type: 2G,3G,4G ex: network_type='"${value}" == "2G"'
                     lac: 1234 ex: lac='${value} == 1234'
                     cell_id: 1234 ex: cell_id='${value} == 1234'
                     status: not_register,registering,connected,disconnected ex: status='"${value}" == "connected"'
                     ip_address: 192.168.2.1 ex: ip_address='"${value}" == "192.168.2.1"'
                     netmask: 255.255.255.0 ex: netmask='"${value}" == "255.255.255.0"'
                     gateway: 192.168.2.1 ex: gateway='"${value}" == "192.168.2.1"'
                     dns:  61.139.2.69 ex: dns='"${value}" == "61.139.2.69"'
                     mtu: 1500 ex: mtu='${value} == 1500'
                     connect_time: 00:00:00 ex: connect_time='"${value}".startswith("00:00")'
        :return:
        """
        self.access_menu('network.network_interface.cellular')
        return self.eval_locator_attribute(kwargs, self.network_locators.cellular_status_locators)

    @allure.step('获取蜂窝信息')
    def get_cellular_status(self, keys: str or list or tuple) -> str or dict or None:
        """

        :param keys:
                     active_sim: SIM 1,SIM 2
                     imei: 123456789012345
                     imsi: 123456789012345
                     iccid: 123456789012345
                     register_status: Registering, 中文情况下返回中文，英文情况下返回英文
                     operator: China Mobile,中文情况下返回中文，英文情况下返回英文
                     network_type: 2G,3G,4G
                     lac: 1234
                     cell_id: 1234
                     status: Registering, 中文情况下返回中文，英文情况下返回英文
                     ip_address: 192.168.2.1
                     netmask: 255.255.255.0
                     gateway: 192.168.2.1
                     dns:  61.139.2.69
                     mtu: 1500
                     connect_time: 00:00:00
        :return: 当key为列表或者元组时， 使用字典返回相关关键字的信息
        """
        self.access_menu('network.network_interface.cellular')
        return self.get_text(keys, self.network_locators.cellular_status_locators)

    @allure.step('配置蜂窝网')
    def config_cellular(self, **kwargs):
        """ 配置蜂窝网参数, 无需配置时均不填写参数

        :param kwargs:
               cellular_enable: enable,disable ex: cellular_enable="enable"
               profile: [($action, **kwarg)]
                  ex: [('delete_all', )],
                 [('delete', '2GSM')]
                 [('add', {'network_type': 'GSM', 'apn': '3gnet', 'access_number': '*99***1#', 'auth_method': 'auto', 'username': 'gprs', 'password': 'gprs'})]
                     add parameter:
                     network_type: GSM,CDMA, ex: network_type="GSM"
                     apn: 3gnet ex: apn="3gnet"
                     access_number: *99***1# ex: access_number="*99***1#"
                     auth_method: auto,PAP,CHAP,MS-CHAP,MS-CHAPv2 ex: auth_method="auto"
                     username: gprs ex: username="gprs"
                     password: gprs ex: password="gprs"
                     error_text: str or list
                     cancel: True, False
                 [('add', {'network_type': 'GSM', 'apn': '3gnet', 'access_number': '*99***1#',
                          'auth_method': 'auto', 'username': 'gprs', 'password': 'gprs', 'is_exists': 'GSM3gnet'})] 如果存在GSM3gnet则不添加
                 [('edit', '2GSM', {'network_type': 'GSM', 'apn': '4gnet'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               dual_sim_enable: enable,disable ex: dual_sim_enable="enable"
               main_sim: SIM1,SIM2,Random,Sequence ex: main_sim="SIM1"
               max_number_of_dial: 10 ex: max_number_of_dial=10
               min_connected_time: 10 ex: min_connected_time=10
               backup_sim_timeout: 10 ex: backup_sim_timeout=10
               network_type: 2G,3G,4G,auto ex: network_type="auto"
               sim1_profile: auto,1,2,3 ex: sim1_profile="auto"
               sim1_roaming: enable,disable ex: sim1_roaming="enable"
               sim1_pincode: 1234 ex: sim1_pincode=1234
               sim1_csq_threshold: 10 ex: sim1_csq_threshold=10
               sim1_csq_detect_interval: 10 ex: sim1_csq_detect_interval=10
               sim1_csq_detect_retries: 10 ex: sim1_csq_detect_retries=10
               sim2_profile: auto,1,2,3 ex: sim2_profile="auto"
               sim2_roaming: enable,disable ex: sim2_roaming="enable"
               sim2_pincode: 1234 ex: sim2_pincode=1234
               sim2_csq_threshold: 10 ex: sim2_csq_threshold=10
               sim2_csq_detect_interval: 10 ex: sim2_csq_detect_interval=10
               sim2_csq_detect_retries: 10 ex: sim2_csq_detect_retries=10
               static_ip_enable:  enable,disable ex: static_ip_enable="enable"
               static_ip: '192.168.2.1' ex: static_ip="192.168.2.1"
               static_peer: '192.168.2.1' ex: static_peer="192.168.2.1"
               radial_interval: 10 ex: radial_interval=10
               icmp_probes: expand,close ex: icmp_probes="expand"
               icmp_detection_server1: '8.8.8.8' ex: icmp_detection_server1="8.8.8.8"
               icmp_detection_server2: '8.8.8.8' ex: icmp_detection_server2="8.8.8.8"
               icmp_detection_interval: 10 ex: icmp_detection_interval=10
               icmp_detection_max_retries: 10 ex: icmp_detection_max_retries=10
               icmp_detection_timeout: 10 ex: icmp_detection_timeout=10
               icmp_detection_strict: enable,disable ex: icmp_detection_strict="enable"
               advanced_settings: 'expand' ex: advanced_settings="expand"
               init_command: 'AT+CPIN?' ex: init_command="AT+CPIN?"
               mru: 1500 ex: mru=1500
               rssi_poll_interval: 10 ex: rssi_poll_interval=10
               mtu: 1500 ex: mtu=1500
               dial_timeout: 10 ex: dial_timeout=10
               use_default_asyncmap: enable,disable ex: use_default_asyncmap="enable"
               use_peer_dns: enable,disable ex: use_peer_dns="enable"
               lcp_interval: 10 ex: lcp_interval=10
               lcp_max_retries: 10 ex: lcp_max_retries=10
               infinitely_dial_retry: enable,disable ex: infinitely_dial_retry="enable"
               debug: enable,disable ex: debug="enable"
               expert_options: 'AT+CPIN?'
               error_text: str or list or tuple ex: error_text="Please enter an integer for 1 ~ 604800"
               submit: True or False ex: submit=True
               profile_save_ok: True or False ex: profile_save_ok=True 点击submit后是否弹出保存成功的提示框
               success_tip: True  保存成功后的提示信息
               reset: True or False ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.cellular')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'cellular_configuration_changed_successful'})
        self.agg_in(self.network_locators.cellular_locators, kwargs)


class Ethernet(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言网络状态')
    @loop_inspector('ethernet_status')
    def assert_ethernet_status(self, port='gigabitethernet 0/1', **kwargs):
        """
        :param port: gigabitethernet 0/1,gigabitethernet 0/2
        :param kwargs:
               network_type: static_ip, dynamic_address_dhcp, ex: network_type='"${value}"=="static_ip"'
               ip_address: 192.168.2.1 ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
               gateway: 192.168.2.1 ex: gateway='"${value}"=="192.168.2.1"'
               dns: 61.139.2.69 ex: dns='"${value}"=="61.139.2.69"'
               mtu: 1500 ex: mtu='"${value}"=="1500"'
               status： up, down ex: status='"${value}"=="up"'
               connection_time: 0 day 00:00:00 ex: connection_time='"${value}".startswith("0 day 00:")'
               description: eth0 ex: description='"${value}"=="eth0"'
        """
        self.access_menu(f'network.network_interface.ethernet.{port}')
        return self.eval_locator_attribute(kwargs, self.network_locators.ethernet_status_locators)

    @allure.step('获取网络状态')
    def get_ethernet_status(self, keys: str or list, port='gigabitethernet 0/1') -> str or dict or None:
        """
        :param port: gigabitethernet 0/1,gigabitethernet 0/2
        :param keys:
               network_type:
               ip_address:
               netmask:
               gateway:
               dns:
               mtu:
               status：
               connection_time:
               description:
        """
        self.access_menu(f'network.network_interface.ethernet.{port}')
        return self.get_text(keys, self.network_locators.ethernet_status_locators)

    @allure.step('配置网络')
    def config_ethernet(self, port='gigabitethernet 0/1', **kwargs):
        """ 配置网络, 在配置网口2 时需要先去网桥关闭网口2桥接口，否则无法配置

        :param port:  gigabitethernet 0/1,gigabitethernet 0/2
        :param kwargs:
                network_type: static_ip, dynamic_address_dhcp, ex: network_type='static_ip'
                ip_address: 192.168.2.1 ex: ip_address='192.168.2.1'
                netmask: 255.255.255.0 ex: netmask='255.255.255.0'
                speed_duplex: auto_negotiation, 1000m full duplex, 1000m half duplex, 100m full duplex, 100m half duplex, 10m full duplex, 10m half duplex
                              ex: speed_duplex='1000m full duplex'
                mtu: 1500 ex: mtu=1500
                track_l2_state: enable, disable ex: track_l2_state='enable'
                shutdown: enable, disable ex: shutdown='enable'
                description: eth0 ex: description='eth0'
                secondary_ip_settings:
                    [($action, **kwarg)]
                    ex: [('delete_all', )],
                     [('delete', '192.168.2.1255.255.255.0')]
                     [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0'})]
                     add parameter:
                        secondary_ip:
                        netmask:
                        error_text: str or list
                        cancel: True, False
                     [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0', 'is_exists': '192.168.2.1255.255.255.0'})]  如果存在就不加
                     [('edit', '192.168.2.1255.255.255.0', {'secondary_ip': '192.168.3.1', 'netmask': '255.255.255.0'})]
                     多个操作时使用列表 [('add',{}), ('add',{})]
                submit: True, False ex: submit=True
                errors_text: 'ip_address_conflict' ex: errors_text='ip_address_conflict'
                success_tip: True ex: success_tip=True 提交后需要验证成功的提示框
                reset: True ex: reset=True
        :return:
        """
        self.access_menu(f'network.network_interface.ethernet.{port}')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        try:
            self.agg_in(self.network_locators.ethernet_locators, kwargs)
        except TimeoutError:
            raise TimeoutError(f'please check bridge member of {port} is enabled or not')


class Bridge(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言网桥接口状态')
    @loop_inspector('bridge_status')
    def assert_bridge_status(self, **kwargs):
        """
        :param kwargs:
               ip_address: 192.168.2.1 ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
               mtu: 1500 ex: mtu='"${value}"=="1500"'
               status： up, down ex: status='"${value}"=="up"'
               connection_time: 0 day 00:00:00 ex: connection_time='"${value}".startswith("0 day 00")'
               description: eth0 ex: description='"${value}"=="eth0"'
        """
        self.access_menu('network.network_interface.bridge')
        return self.eval_locator_attribute(kwargs, self.network_locators.bridge_status_locators)

    @allure.step('获取网桥接口状态')
    def get_bridge_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               ip_address:
               netmask:
               mtu:
               status：
               connection_time:
               description:
        """
        self.access_menu('network.network_interface.bridge')
        return self.get_text(keys, self.network_locators.bridge_status_locators)

    @allure.step('配置网桥接口')
    def config_bridge(self, **kwargs):
        """ 配置网桥接口

        :param kwargs:
                ip_address: 192.168.2.1 ex: ip_address='192.168.2.1'
                netmask: 255.255.255.0 ex: netmask='255.255.255.0'
                description: eth0 ex: description='eth0'
                secondary_ip_settings:
                [($action, **kwarg)] ex: [('delete_all', )],
                 [('delete', '192.168.2.1255.255.255.0')]
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0'})]
                    add parameter:
                    secondary_ip:
                    netmask:
                    error_text: str or list
                    cancel: True, False
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0', 'is_exists': '192.168.2.1255.255.255.0'})]  如果存在就不加
                 [('edit', '192.168.2.1255.255.255.0', {'secondary_ip': '192.168.3.1', 'netmask': '255.255.255.0'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
                ge_01: enable, disable ex: ge_01='enable'
                ge_02: enable, disable ex: ge_02='enable'
                submit: True, False ex: submit=True
                errors_text: 'ip_address_conflict' ex: errors_text='ip_address_conflict'
                success_tip: True ex: success_tip=True 提交后需要验证成功的提示框
                reset: True ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.bridge')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.bridge_locators, kwargs)


class Wlan(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言WLAN状态')
    @loop_inspector('wlan_status')
    def assert_wlan_status(self, **kwargs):
        """
        :param kwargs:
               station_role: ap,client ex: station_role='"${value}"=="ap"'
               wlan_status: enable, disable ex: wlan_status='"${value}"=="enable"'
               mac_address: 00:00:00:00:00:00 ex: mac_address='"${value}"=="00:00:00:00:00:00"'
               ssid: inhand-xxxx ex: ssid='"${value}"=="inhand-xxxx"'
               channel: 1,2,3,4,5,6,7,8,9,10,11 ex: channel='"${value}"=="1"'
               auth_method: OPEN, SHARED, WPA-PSK, WPA, WPA2-PSK, WPA2, WPAPSK/WPA2PSK ex: auth_method='"${value}"=="OPEN"'
               encrypt_mode: TKIP, AES, NONE, WEP40,  WEP104 ex: encrypt_mode='"${value}"=="TKIP"'
               ip_address: 192.168.2.1, ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
               gateway: 192.168.2.1 ex: gateway='"${value}"=="192.168.2.1"'
               dns: 61.139.2.69 ex: dns='"${value}"=="61.139.2.69"'
               wireless_connection_status: connect, disconnect ex: wireless_connection_status='"${value}"=="connect"'
               connection_time: 0 day 00:00:00 ex: connection_time='"${value}".startswith("0 day 00")'
        """
        self.access_menu('network.network_interface.wlan')
        return self.eval_locator_attribute(kwargs, self.network_locators.wlan_status_locators)

    @allure.step('获取WLAN状态')
    def get_wlan_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               station_role:
               wlan_status:
               mac_address:
               ssid：
               channel:
               auth_method:
               encrypt_mode
               ip_address
               netmask
               gateway
               dns
               wireless_connection_status
               connection_time
        """
        self.access_menu('network.network_interface.wlan')
        return self.get_text(keys, self.network_locators.wlan_status_locators)

    @allure.step('配置WLAN')
    def config_wlan(self, **kwargs):
        """如遇到需要等待的情况，自行在添加，不在通用方法中添加， 该方法也可以分拆成多个步骤执行

        :param kwargs:
               enable_wifi: enable,disable ex: enable_wifi="enable"
               station_role: ap,client ex: station_role="ap"
               sta_default_route: enable,disable ex: sta_default_route="enable"
               sta_ssid: inhand-xxxx ex: sta_ssid="inhand-xxxx"
               sta_scan: {'wait_for_time': 5*1000}, False ex: sta_scan={'wait_for_time': 5*1000} 点击完扫描后会等待5s
               sta_connect: 'inhand-visitor80:8d:b7:eb:80:90'
               sta_auth_method: OPEN, SHARED, WPA-PSK, WPA, WPA2-PSK, WPA2 ex: sta_auth_method="OPEN"
               sta_encrypt_mode: TKIP, AES, NONE, WEP40,  WEP104, ex: sta_encrypt_mode="TKIP"
               sta_wpa_psk: 12345678 ex: sta_wpa_psk="12345678"
               sta_wpa_psk_key: 12345678 ex: sta_wpa_psk_key="12345678"
               sta_auth_mode: EAP-PEAP, EAP-TLS ex: sta_auth_mode="EAP-PEAP"
               sta_inner_auth: mschapv2, md5, ex: sta_inner_auth="mschapv2"
               sta_username: inhand ex: sta_user_name="inhand"
               sta_password: inhand ex: sta_password="inhand"
               sta_network_type: static_ip, dynamic_address_dhcp ex: sta_network_type="static_ip"
               sta_ip_address: 192.168.3.1 ex: sta_ip_address="192.168.3.1"
               sta_netmask: 255.255.255.0, ex: sta_netmask="255.255.255.0"

               ap_ssid_broadcast: enable,disable ex: ap_ssid_broadcast="enable"
               ap_bridge: enable,disable ex: ap_bridge="enable"
               ap_band: 2.4G,5G ex: ap_band="2.4G"
               ap_radio_type: 802.11b/g,802.11b,802.11g,802.11n,802.11g/n,802.11b/g/n  ex: ap_radio_type="802.11b/g/n"
               ap_channel: 1,2,3,4,5,6,7,8,9,10,11,12,13 ex: ap_channel="1"
               ap_ssid: inhand-xxxx ex: ap_ssid="inhand-xxxx"
               ap_auth_method: OPEN, SHARED, WPA-PSK, WPAPSK/WPA2PSK, ex: ap_auth_method="OPEN"
               ap_encrypt_mode: TKIP, AES, NONE, WEP40,  WEP104, ex: ap_encrypt_mode="TKIP"
               ap_wep_key: 123456, ex: ap_wep_key="123456"
               ap_wpa_psk_key: 12345678, ex: ap_wpa_psk_key="12345678"
               ap_bandwidth: 20MHz,40MHz, ex: ap_bandwidth="20MHz"
               ap_stations_limit: 1,2,3,4,5,6,7,8,9,10, ex: ap_stations_limit="1"
               submit: True,False ex: submit=True
               errors_text: 'ip_address_conflict' ex: errors_tip='ip_address_conflict'
               success_tip: True,False ex: success_tip=True
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.wlan')
        if kwargs.get('sta_connect'):
            kwargs.update({'sta_connect': [('connect', kwargs.get('sta_connect'))]})
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.wlan_locators, kwargs)


class Wan(BasePage, IgLocators):
    __doc__ = 'IG502 function: wan'

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG502', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言WAN状态')
    @loop_inspector('wan_status')
    def assert_wan_status(self, **kwargs):
        """
        :param kwargs:
               network_type: static_ip,dynamic_address_dhcp ex: network_type='"${value}"=="static_ip"'
               ip_address: 192.168.2.1, ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
               gateway: 192.168.2.1 ex: gateway='"${value}"=="192.168.2.1"'
               dns: 61.139.2.69 ex: dns='"${value}"=="61.139.2.69"'
               mtu: 1500 ex: mtu='"${value}"=="1500"'
               status: up, down ex: status='"${value}"=="up"'
               description: ex: description='"${value}"=="WAN1"'
               connection_time: 0 day 00:00:00 ex: connection_time='"${value}".startswith("0 day 00:00")'
        """
        self.access_menu('network.network_interface.wan')
        return self.eval_locator_attribute(kwargs, self.network_locators.wan_status_locators)

    @allure.step('获取WAN状态')
    def get_wan_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               network_type, ip_address, netmask, gateway, dns, mtu, status, description, connection_time
        """
        self.access_menu('network.network_interface.wan')
        return self.get_text(keys, self.network_locators.wan_status_locators)

    @allure.step('配置WAN')
    def config_wan(self, **kwargs):
        """

        :param kwargs:
               interface_type: WAN,LAN ex: interface_type='WAN'
               network_type: static_ip,dynamic_address_dhcp ex: network_type='static_ip'
               ip_address: 192.168.2.1, ex: ip_address='192.168.2.1'
               netmask: 255.255.255.0, ex: netmask='255.255.255.0'
               gateway: 192.168.2.1, ex: gateway='192.168.2.1'
               dns: 8.8.8.8 ex: dns='8.8.8.8'
               mtu: 1500 ex: mtu='1500'
               track_l2_state: enable,disable ex: track_l2_state='enable'
               shutdown: enable,disable ex: shutdown='enable'
               description: ex: description='WAN1'
               secondary_ip_settings:
               [($action, **kwarg)] ex: [('delete_all', )],
                 [('delete', '192.168.2.1255.255.255.0')]
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0'})]
                 add parameter:
                    secondary_ip:
                    netmask:
                    errors_text
                    cancel: True,
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0', 'is_exists': '192.168.2.1255.255.255.0'})]  如果存在就不加
                 [('edit', '192.168.2.1255.255.255.0', {'secondary_ip': '192.168.3.1', 'netmask': '255.255.255.0'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               submit: True,False ex: submit=True
               errors_text: 'ip_address_conflict' ex: errors_text='ip_address_conflict'
               success_tip: True,False ex: success_tip=True
                reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.wan')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.wan_locators, kwargs)


class Lan(BasePage, IgLocators):
    __doc__ = 'IG502 function: lan'

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG502', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言LAN状态')
    @loop_inspector('lan_status')
    def assert_lan_status(self, **kwargs):
        """
        :param kwargs:
               ip_address: 192.168.2.1, ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
               mtu: 1500 ex: mtu='"${value}"=="1500"'
               status: up, down ex: status='"${value}"=="up"'
               description: ex: description='"${value}"=="WAN1"'
               connection_time: 0 day 00:00:00 ex: connection_time='"${value}".startswith("0 day 00:00")'
        """
        self.access_menu('network.network_interface.lan')
        return self.eval_locator_attribute(kwargs, self.network_locators.lan_status_locators)

    @allure.step('获取LAN状态')
    def get_lan_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               ip_address, netmask, mtu, status, description, connection_time
        """
        self.access_menu('network.network_interface.lan')
        return self.get_text(keys, self.network_locators.lan_status_locators)

    @allure.step('配置LAN')
    def config_lan(self, **kwargs):
        """

        :param kwargs:
               ip_address: 192.168.2.1, ex: ip_address='192.168.2.1'
               netmask: 255.255.255.0, ex: netmask='255.255.255.0'
               shutdown: enable,disable ex: shutdown='enable'
               description: ex: description='WAN1'
               secondary_ip_settings:
               [($action, **kwarg)] ex: [('delete_all', )],
                 [('delete', '192.168.2.1255.255.255.0')]
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0'})]
                    add parameter:
                        secondary_ip:
                        netmask:
                        errors_text: str or list
                        cancel: True,
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0', 'is_exists': '192.168.2.1255.255.255.0'})]  如果存在就不加
                 [('edit', '192.168.2.1255.255.255.0', {'secondary_ip': '192.168.3.1', 'netmask': '255.255.255.0'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               submit: True,False ex: submit=True
               errors_text: 'ip_address_conflict' ex: errors_text='ip_address_conflict'
               success_tip: True,False ex: success_tip=True
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.lan')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.lan_locators, kwargs)


class Loopback(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG502', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言Loopback状态')
    @loop_inspector('loopback_status')
    def assert_loopback_status(self, **kwargs):
        """
        :param kwargs:
               ip_address: 192.168.2.1, ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
        """
        self.access_menu('network.network_interface.loopback')
        return self.eval_locator_attribute(kwargs, self.network_locators.loopback_status_locators)

    @allure.step('获取Loopback状态')
    def get_loopback_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               ip_address, netmask
        """
        self.access_menu('network.network_interface.loopback')
        return self.get_text(keys, self.network_locators.loopback_status_locators)

    @allure.step('配置Loopback')
    def config_loopback(self, **kwargs):
        """

        :param kwargs:
               secondary_ip_settings:
               [($action, **kwarg)] ex: [('delete_all', )],
                 [('delete', '192.168.2.1255.255.255.0')]
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0'})]
                    add parameter:
                        secondary_ip:
                        netmask:
                        errors_text: str or list
                        cancel: True,
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0', 'is_exists': '192.168.2.1255.255.255.0'})]  如果存在就不加
                 [('edit', '192.168.2.1255.255.255.0', {'secondary_ip': '192.168.3.1', 'netmask': '255.255.255.0'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               submit: True,False ex: submit=True
               errors_text: 'ip_address_conflict' ex: errors_text='ip_address_conflict'
               success_tip: True,False ex: success_tip=True
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.loopback')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.loopback_locators, kwargs)
