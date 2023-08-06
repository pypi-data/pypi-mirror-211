# -*- coding: utf-8 -*-
# @Time    : 2023/5/17 11:54:34
# @Author  : Pane Li
# @File    : ethernet_locators.py
"""
ethernet_locators

"""

from playwright.sync_api import Page


class EthernetLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def ethernet_status_locators(self) -> list:
        return [
            ('network_type', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.network_type}"]]/div[2]'),
                'type': 'text', 'param': {'static_ip': self.locale.static_ip,
                                          'dynamic_address_dhcp': self.locale.dynamic_address_dhcp}}),
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
            ('status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.status}"]]/div[2]'),
                'type': 'text', 'param': {'up': 'Up', 'down': 'Down'}}),
            ('connection_time', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.connection_time}"]]/div[2]'),
                'type': 'text', 'param': {'day': self.locale.day}}),
            ('description', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.description}"]]/div[2]'),
                'type': 'text'}),
        ]

    @property
    def ethernet_locators(self) -> list:
        return [
            ('network_type', {'locator': self.page.locator('#internet'), 'type': 'select',
                              'param': {'static_ip': self.locale.static_ip,
                                        'dynamic_address_dhcp': self.locale.dynamic_address_dhcp}}),
            ('ip_address', {'locator': self.page.locator('#primary_ip'), 'type': 'text'}),
            ('netmask', {'locator': self.page.locator('#netmask'), 'type': 'text'}),
            ('speed_duplex', {'locator': self.page.locator('#speed_duplex'), 'type': 'select',
                              'param': {'auto_negotiation': self.locale.auto_negotiation, 'full': self.locale.full,
                                        'half': self.locale.half, 'duplex': self.locale.duplex, 'm': 'M'}}),
            ('mtu', {'locator': self.page.locator('#mtu'), 'type': 'text'}),
            ('track_l2_state', {'locator': self.page.locator('#track_l2_state'), 'type': 'switch_button'}),
            ('shutdown', {'locator': self.page.locator('#shutdown'), 'type': 'switch_button'}),
            ('description', {'locator': self.page.locator('#description'), 'type': 'text'}),
            ('secondary_ip_settings', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('secondary_ip', {'locator': self.pop_up.locator('#secondary_ip'), 'type': 'text'}),
                    ('netmask',
                     {'locator': self.pop_up.locator('#netmask'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]
