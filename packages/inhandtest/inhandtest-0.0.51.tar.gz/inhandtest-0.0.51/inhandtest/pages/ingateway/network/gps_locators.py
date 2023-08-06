# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 16:41:50
# @Author  : Pane Li
# @File    : gps_locators.py
"""
gps_locators

"""
from playwright.sync_api import Page


class GpsLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def gps_status_locators(self) -> list:
        return [
            ('gps_status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.gps_status}"]]/div[2]'),
                'type': 'text', 'param': {'enable': self.locale.enable, 'disable': self.locale.disable}}),
            ('time_', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.time}"]]/div[2]'),
                'type': 'text', 'param': {'day': self.locale.day}}),
            ('location', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.location}"]]/div[2]'),
                'type': 'text'}),
            ('speed', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.speed}"]]/div[2]'),
                'type': 'text'}),
        ]

    @property
    def gps_locators(self) -> list:
        return [
            ('enable', {'locator': self.page.locator(f'//button'), 'type': 'switch_button'})
        ]

    @property
    def gps_ip_forwarding_locators(self) -> list:
        return [
            ('enable', {'locator': self.page.locator(f'#enable'), 'type': 'switch_button'}),
            ('type_', {'locator': self.page.locator('#type'), 'type': 'select',
                       'param': {'client': self.locale.client, 'server': self.locale.server},
                       'relation': [('enable', True)]}),
            ('transmit_protocol', {'locator': self.page.locator('#client_transmit_proto'), 'type': 'select',
                                   'relation': [('enable', True)]}),
            ('connection_type', {'locator': self.page.locator('#connect_type'), 'type': 'select',
                                 'param': {'long_lived': self.locale.long_lived,
                                           'short_lived': self.locale.short_lived},
                                 'relation': [('enable', True)]}),
            ('keepalive_interval',
             {'locator': self.page.locator('#keepalive_interval'), 'type': 'text', 'relation': [('enable', True)]}),
            ('keepalive_retry',
             {'locator': self.page.locator('#keepalive_retry'), 'type': 'text', 'relation': [('enable', True)]}),
            ('idle_timeout',
             {'locator': self.page.locator('#idle_time'), 'type': 'text', 'relation': [('enable', True)]}),
            ('local_port',
             {'locator': self.page.locator('#server_local_port'), 'type': 'text', 'relation': [('enable', True)]}),
            ('min_reconnect_interval',
             {'locator': self.page.locator('#client_min_reconnect_interval'), 'type': 'text',
              'relation': [('enable', True)]}),
            ('max_reconnect_interval',
             {'locator': self.page.locator('#client_max_reconnect_interval'), 'type': 'text',
              'relation': [('enable', True)]}),
            ('source_interface', {'locator': self.page.locator('#client_source_interface'), 'type': 'select',
                                  'relation': [('enable', True)]}),
            ('reporting_interval', {'locator': self.page.locator('#trap_interval'), 'type': 'text',
                                    'relation': [('enable', True)]}),
            ('include_rmc', {'locator': self.page.locator('#rmc'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gsa', {'locator': self.page.locator('#gsa'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gga', {'locator': self.page.locator('#gga'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gsv', {'locator': self.page.locator('#gsv'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('message_prefix', {'locator': self.page.locator('#prefix'), 'type': 'text',
                                'relation': [('enable', True)]}),
            ('message_suffix', {'locator': self.page.locator('#suffix'), 'type': 'text',
                                'relation': [('enable', True)]}),
            ('destination_ip_address', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('server',
                     {'locator': self.page.locator('.ant-modal-content').locator('#server_ip'), 'type': 'text'}),
                    ('port',
                     {'locator': self.page.locator('.ant-modal-content').locator('#server_port'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]

    @property
    def gps_serial_forwarding_locators(self) -> list:
        return [
            ('enable', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('serial_type',
             {'locator': self.page.locator('#serial_type'), 'type': 'select', 'relation': [('enable', True)]}),
            ('baudrate',
             {'locator': self.page.locator('#baudrate'), 'type': 'select', 'relation': [('enable', True)]}),
            ('data_bits',
             {'locator': self.page.locator('#data_bits'), 'type': 'select', 'relation': [('enable', True)]}),
            ('parity',
             {'locator': self.page.locator('#parity'), 'type': 'select', 'relation': [('enable', True)],
              'param': {'none': self.locale.none, 'even': self.locale.even, 'odd': self.locale.odd}}),
            ('stop_bit',
             {'locator': self.page.locator('#stop_bit'), 'type': 'select', 'relation': [('enable', True)]}),
            ('software_flow_control',
             {'locator': self.page.locator('#soft_flow_control'), 'type': 'switch_button',
              'relation': [('enable', True)]}),
            ('include_rmc', {'locator': self.page.locator('#rmc'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gsa', {'locator': self.page.locator('#gsa'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gga', {'locator': self.page.locator('#gga'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gsv', {'locator': self.page.locator('#gsv'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]
