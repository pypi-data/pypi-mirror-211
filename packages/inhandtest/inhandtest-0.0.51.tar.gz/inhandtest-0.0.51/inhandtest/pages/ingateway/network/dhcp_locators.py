# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 16:41:30
# @Author  : Pane Li
# @File    : dhcp_locators.py
"""
dhcp_locators

"""
from playwright.sync_api import Page


class DhcpLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def dhcp_locators(self) -> list:
        return [
            ('dhcp_server', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox').nth(0),
                "columns": [
                    ('enable_dhcp_server',
                     {'locator': self.page.locator('.ant-modal-content').locator('#enable'), 'type': 'switch_button'}),
                    ('interface',
                     {'locator': self.page.locator('.ant-modal-content').locator('#interface'), 'type': 'select'}),
                    ('start_address',
                     {'locator': self.page.locator('.ant-modal-content').locator('#start_addr'), 'type': 'text'}),
                    ('end_address',
                     {'locator': self.page.locator('.ant-modal-content').locator('#end_addr'), 'type': 'text'}),
                    ('lease',
                     {'locator': self.page.locator('.ant-modal-content').locator('#lease'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr'}),
            ('windows_name_server', {'locator': self.page.locator('#windows_name_server'), 'type': 'text'}),
            ('static_ip_setting', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox').nth(1),
                "columns": [
                    ('mac_address', {'locator': self.pop_up.locator('#mac_addr'), 'type': 'text'}),
                    ('ip_address', {'locator': self.pop_up.locator('#ip_addr'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr', 'param': {'enable': self.locale.enable, 'not_enable': self.locale.not_enable}}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]
