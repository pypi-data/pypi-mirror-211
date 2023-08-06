# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 16:41:40
# @Author  : Pane Li
# @File    : dns_locators.py
"""
dns_locators

"""
from playwright.sync_api import Page


class DnsLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def dns_locators(self) -> list:
        return [
            ('primary_dns', {'locator': self.page.locator('#primary_dns'), 'type': 'text'}),
            ('secondary_dns', {'locator': self.page.locator('#secondary_dns'), 'type': 'text'}),
            ('submit_dns_server',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit).nth(0),
              'type': 'button'}),
            ('enable_dns_relay', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('domain_ip_address_pair', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('host',
                     {'locator': self.pop_up.locator('#host'), 'type': 'text'}),
                    ('ip_address1', {'locator': self.pop_up.locator('#ip_addr1'), 'type': 'text'}),
                    ('ip_address2', {'locator': self.pop_up.locator('#ip_addr2'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr'}),
            ('submit_domain_ip_address_pair',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit).nth(1),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]
