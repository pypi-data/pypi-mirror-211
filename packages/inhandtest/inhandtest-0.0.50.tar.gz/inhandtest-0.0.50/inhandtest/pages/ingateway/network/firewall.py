# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 15:34:57
# @Author  : Pane Li
# @File    : firewall.py
"""
firewall

"""
import allure
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators


class Acl(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置ACL规则')
    def config_acl(self, default_filter_strategy='permit', **kwargs):
        """
        :param default_filter_strategy: 'permit', 'deny',
        :param kwargs:
               access_control_strategy: [($action, **kwarg)] ex: [('delete_all', )],
                    [('delete', '10010')]
                    [('add', {'acl_type': 'standard', 'id': 100,'sequence_number': 40, 'action': 'permit', 'protocol': 'IP',})]
                    add parameters:
                        acl_type: 'standard', 'extended'
                        id: int
                        sequence_number: 1-100
                        action: 'permit', 'deny'
                        protocol: 'IP', 'ICMP', 'TCP', 'UDP', 'GRE', 'ESP', 'AH', 'OSPF', 'L2TpV3', '1-255'
                        protocol_id: 1-255
                        source_ip: '1.1.1.1'
                        source_wildcard: str
                        source_port: Any,=,!=,>,<,Range
                        source_port_value: 1-65535
                        source_port_value1: 1-65535
                        destination_ip:  '1.1.1.1'
                        destination_wildcard: str
                        destination_port: Any,=,!=,>,<,Range
                        destination_port_value: 1-65535
                        destination_port_value1: 1-65535
                        icmp_type: used_describe, use_type_code
                        icmp_describe:  'all' or other
                        icmp_type_value:  str
                        icmp_code: str
                        fragments: enable, disable
                        established: enable, disable
                        log: enable, disable
                        destination: str
                        error_text: str or list
                        cancel: True, False
                    [('add', {'acl_type': 'standard', 'id': 100, 'sequence_number': 40, 'is_exists': '10040'})] 如果存在则不添加
                    [('edit', '10040', {'sequence_number': 60})]
               access_control_list: [($action, **kwarg)] ex: [('delete_all', )],
                    [('delete', 'Cellular 1')]
                    [('add', {'interface': 'Cellular 1', 'in_acl': '100','out_acl': '102', 'admin_acl': '104'})]
                    add parameters:
                        interface: 'Cellular 1', 'Bridge 1', 'Openvpn 1', 'Gigabitethernet 0/1', 'Gigabitethernet 0/2',
                        in_acl: 100
                        out_acl: 100
                        admin_acl: 102
                        error_text: str or list
                        cancel: True, False
                    [('add', {'interface': 'Cellular 1', 'in_acl': 100, 'out_acl': 102, 'is_exists': 'Cellular 1'})] 如果存在则不添加
                    [('edit', 'Cellular 1', {'in_acl': 102})]
              submit: True,False ex: submit=True
              error_text: str ex: error_text='ip_address_conflict'
              success_tip: True
              reset: True, False ex: reset=True
        """
        self.access_menu('network.firewall.acl')
        self.agg_in(self.network_locators.acl_locators, {'default_filter_strategy': default_filter_strategy}),
        if kwargs:
            if kwargs.get('success_tip'):
                kwargs.update({'success_tip': 'submit_success'})
            self.agg_in(self.network_locators.acl_locators, kwargs)


class Nat(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置NAT规则')
    def config_nat(self, **kwargs):
        """

        :param kwargs:
               nat_rules: [($action, **kwarg)] ex: [('delete_all', )],
                    [('delete', 'SNAT.*ACL:100')]
                    [('add', {'action': 'SNAT', 'source_network': 'inside', 'translation_type': 'IP to IP'})]
                    add parameters:
                        action: SNAT, DNAT, 1:1NAT
                        source_network: 'inside', 'outside'
                        translation_type: IP to IP, IP to INTERFACE, IP PORT to IP PORT, ACL to INTERFACE, ACL to IP, INTERFACE to IP, INTERFACE PORT to IP PORT, Virtual IP to IP, Virtual IP to INTERFACE,
                        transmit_protocol: TCP, UDP
                        match_ip: str
                        match_port: str
                        match_end_port: str
                        match_acl: str
                        match_interface: 'Cellular 1'
                        virtual_ip: str
                        real_ip: str
                        interface: 'Cellular 1'
                        translated_ip: str
                        translated_interface: 'Cellular 1'
                        translated_port: str
                        translated_end_port: str
                        source_ip: str
                        source_netmask: str
                        log: enable, disable
                        destination: str
                        error_text: str or list
                        cancel: True, False
                    [('add', {'action': 'SNAT', 'source_network': 'inside', 'translation_type': 'IP to IP', 'is_exists': 'SNAT.*ACL:100'})] 如果存在则不添加
                    [('edit', 'SNAT.*ACL:100', {'action': 'SNAT'})]
               network_interface: [($action, **kwarg)] ex: [('delete_all', )],
                    [('delete', 'Cellular 1')]
                    [('add', {'interface': 'Cellular 1', 'interface_type': 'inside'})]
                    add parameters:
                        interface: 'Cellular 1', 'Bridge 1', 'Openvpn 1', 'Gigabitethernet 0/1', 'Gigabitethernet 0/2',
                        interface_type: inside, outside
                        error_text: str or list
                        cancel: True, False
                    [('add', {'interface': 'Cellular 1', 'interface_type': 'inside', 'is_exists': 'Cellular 1'})] 如果存在则不添加
                    [('edit', 'Cellular 1', {'interface_type': 'outside'})]
              submit: True,False ex: submit=True
              error_text: str ex: error_text='ip_address_conflict'
              success_tip: True
              reset: True, False ex: reset=True
        """
        if kwargs:
            self.access_menu('network.firewall.nat')
            if kwargs.get('success_tip'):
                kwargs.update({'success_tip': 'submit_success'})
            self.agg_in(self.network_locators.nat_locators, kwargs)
