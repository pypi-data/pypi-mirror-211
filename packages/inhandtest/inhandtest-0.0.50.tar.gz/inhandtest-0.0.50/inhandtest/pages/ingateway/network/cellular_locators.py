# -*- coding: utf-8 -*-
# @Time    : 2023/5/17 13:43:07
# @Author  : Pane Li
# @File    : cellular_locators.py
"""
cellular_locators

"""
from playwright.sync_api import Page


class CellularLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def cellular_status_locators(self) -> list:
        return [
            ('active_sim', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.active_sim}"]]/div[2]'),
                'type': 'text', 'param': {'sim': 'SIM'}}),
            ('imei', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.imei_code}"]]/div[2]'),
                'type': 'text'}),
            ('imsi', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.imsi_code}"]]/div[2]'),
                'type': 'text'}),
            ('iccid', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.iccid_code}"]]/div[2]'),
                'type': 'text'}),
            ('register_status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.register_status}"]]/div[2]'),
                'type': 'text',
                'param': {'not_register': self.locale.not_register, 'registering': self.locale.registering,
                          'disconnected': self.locale.disconnect, 'connected': self.locale.connect}}),
            ('operator', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.operator}"]]/div[2]'),
                'type': 'text'}),
            ('network_type', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.network_type}"]]/div[2]'),
                'type': 'text'}),
            ('lac', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.lac}"]]/div[2]'),
                'type': 'text'}),
            ('cell_id', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.cell_id}"]]/div[2]'),
                'type': 'text'}),
            ('status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.status}"]]/div[2]'),
                'type': 'text',
                'param': {'not_register': self.locale.not_register, 'registering': self.locale.registering,
                          'disconnected': self.locale.disconnect, 'connected': self.locale.connect}}),
            ('ip_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.ip_address}"]]/div[2]'),
                'type': 'text'}),
            ('netmask', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.netmask}"]]/div[2]'),
                'type': 'text'}),
            ('gateway', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.gateway}"]]/div[2]'),
                'type': 'text'}),
            ('dns', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.dns}"]]/div[2]'),
                'type': 'text'}),
            ('mtu', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.mtu}"]]/div[2]'),
                'type': 'text'}),
            ('connection_time', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.connection_time}"]]/div[2]'),
                'type': 'text'}),
        ]

    @property
    def cellular_locators(self) -> list:
        return [
            ('cellular_enable', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('profile', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('network_type', {'locator': self.pop_up.locator('#network_type'), 'type': 'select'}),
                    ('apn', {'locator': self.pop_up.locator('#apn'), 'type': 'text'}),
                    ('access_number', {'locator': self.pop_up.locator('#access_number'), 'type': 'text'}),
                    ('auth_method', {'locator': self.pop_up.locator('#auth_method'), 'type': 'select',
                                     'param': {'auto': self.locale.auto}}),
                    ('username', {'locator': self.pop_up.locator('#username'), 'type': 'text'}),
                    ('password', {'locator': self.pop_up.locator('#password'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr', 'relation': [('cellular_enable', 'enable')]}),
            ('dual_sim_enable', {'locator': self.page.locator('#enable_dual_sim'), 'type': 'switch_button',
                                 'relation': [('cellular_enable', 'enable')]}),
            ('main_sim', {'locator': self.page.locator('#main_sim'), 'type': 'select',
                          'param': {'Random': self.locale.random, 'Sequence': self.locale.sequence},
                          'relation': [('cellular_enable', 'enable'), ('dual_sim_enable', 'enable')]}),
            ('max_number_of_dial', {'locator': self.page.locator('#max_dial_times'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable'), ('dual_sim_enable', 'enable')]}),
            ('min_connected_time', {'locator': self.page.locator('#min_dial_times'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable'), ('dual_sim_enable', 'enable')]}),
            ('backup_sim_timeout', {'locator': self.page.locator('#backup_sim_timeout'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable'), ('dual_sim_enable', 'enable')]}),
            ('network_type', {'locator': self.page.locator('#network_type').first, 'type': 'select',
                              'param': {'auto': self.locale.auto}, 'relation': [('cellular_enable', 'enable')]}),
            ('sim1_profile', {'locator': self.page.locator('#sim1_profile'), 'type': 'select',
                              'param': {'auto': self.locale.auto}, 'relation': [('cellular_enable', 'enable')]}),
            ('sim1_roaming', {'locator': self.page.locator('#sim1_roaming'), 'type': 'switch_button',
                              'relation': [('cellular_enable', 'enable')]}),
            ('sim1_pincode', {'locator': self.page.locator('#sim1_pincode'), 'type': 'text',
                              'relation': [('cellular_enable', 'enable')]}),
            ('sim1_csq_threshold', {'locator': self.page.locator('#sim1_csq_threshold'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable')]}),
            ('sim1_csq_detect_interval', {'locator': self.page.locator('#sim1_csq_detect_interval'), 'type': 'text',
                                          'relation': [('cellular_enable', 'enable')]}),
            ('sim1_csq_detect_retries', {'locator': self.page.locator('#sim1_csq_detect_retries'), 'type': 'text',
                                         'relation': [('cellular_enable', 'enable')]}),
            ('sim2_profile', {'locator': self.page.locator('#sim2_profile'), 'type': 'select',
                              'param': {'auto': self.locale.auto}, 'relation': [('cellular_enable', 'enable')]}),
            ('sim2_roaming', {'locator': self.page.locator('#sim2_roaming'), 'type': 'switch_button',
                              'relation': [('cellular_enable', 'enable')]}),
            ('sim2_pincode', {'locator': self.page.locator('#sim2_pincode'), 'type': 'text',
                              'relation': [('cellular_enable', 'enable')]}),
            ('sim2_csq_threshold', {'locator': self.page.locator('#sim2_csq_threshold'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable')]}),
            ('sim2_csq_detect_interval', {'locator': self.page.locator('#sim2_csq_detect_interval'), 'type': 'text',
                                          'relation': [('cellular_enable', 'enable')]}),
            ('sim2_csq_detect_retries', {'locator': self.page.locator('#sim2_csq_detect_retries'), 'type': 'text',
                                         'relation': [('cellular_enable', 'enable')]}),
            ('static_ip_enable', {'locator': self.page.locator('#static_ip'), 'type': 'switch_button',
                                  'relation': [('cellular_enable', 'enable')]}),
            ('static_ip', {'locator': self.page.locator('#ip_addr'), 'type': 'text',
                           'relation': [('cellular_enable', 'enable'), ('static_ip_enable', 'enable')]}),
            ('static_peer', {'locator': self.page.locator('#peer_addr'), 'type': 'text',
                             'relation': [('cellular_enable', 'enable'), ('static_ip_enable', 'enable')]}),
            ('radial_interval', {'locator': self.page.locator('#peer_addr'), 'type': 'text',
                                 'relation': [('cellular_enable', 'enable')]}),
            ('icmp_probes', {'locator': self.locale.icmp_probes,
                             'type': 'expand', 'relation': [('cellular_enable', 'enable')]}),
            ('icmp_detection_server1', {'locator': self.page.locator('#icmp.dest_addr1'), 'type': 'text',
                                        'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('icmp_detection_server2', {'locator': self.page.locator('#icmp.dest_addr2'), 'type': 'text',
                                        'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('icmp_detection_interval', {'locator': self.page.locator('#icmp.interval'), 'type': 'text',
                                         'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('icmp_detection_max_retries', {'locator': self.page.locator('#icmp.retires'), 'type': 'text',
                                            'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('icmp_detection_timeout', {'locator': self.page.locator('#icmp.timeout'), 'type': 'text',
                                        'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('icmp_detection_strict', {'locator': self.page.locator('#icmp.strict'), 'type': 'switch_button',
                                       'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('advanced_settings', {'locator': self.locale.advanced_settings,
                                   'type': 'expand', 'relation': [('cellular_enable', 'enable')]}),
            ('init_command', {'locator': self.page.locator('#init_command'), 'type': 'text',
                              'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('mru', {'locator': self.page.locator('#mru'), 'type': 'text',
                     'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('rssi_poll_interval', {'locator': self.page.locator('#rssi_poll_interval'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('mtu', {'locator': self.page.locator('#mtu'), 'type': 'text',
                     'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('dial_timeout', {'locator': self.page.locator('#dial_timeout'), 'type': 'text',
                              'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('use_default_asyncmap', {'locator': self.page.locator('#use_default_asyncmap'), 'type': 'switch_button',
                                      'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('use_peer_dns', {'locator': self.page.locator('#use_peer_dns'), 'type': 'switch_button',
                              'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('lcp_interval', {'locator': self.page.locator('#lcp_interval'), 'type': 'text',
                              'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('lcp_max_retries', {'locator': self.page.locator('#lcp_max_retries'), 'type': 'text',
                                 'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('infinitely_dial_retry', {'locator': self.page.locator('#infinitely_dial_retry'), 'type': 'switch_button',
                                       'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('debug', {'locator': self.page.locator('#debug'), 'type': 'switch_button',
                       'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('expert_options', {'locator': self.page.locator('#expert_options'), 'type': 'text',
                                'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('profile_save_ok',
             {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn ant-btn-primary"]'),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]
