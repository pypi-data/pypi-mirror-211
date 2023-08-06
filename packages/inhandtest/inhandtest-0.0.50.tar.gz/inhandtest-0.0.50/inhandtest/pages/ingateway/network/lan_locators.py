# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 16:13:36
# @Author  : Pane Li
# @File    : lan_locators.py
"""
lan_locators

"""
from playwright.sync_api import Page


class LanLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def lan_status_locators(self) -> list:
        return [
            ('ip_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.ip_address}"]]/div[2]'),
                'type': 'text'}),
            ('netmask', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.netmask}"]]/div[2]'),
                'type': 'text'}),
            ('mtu', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.mtu}"]]/div[2]'),
                'type': 'text', }),
            ('status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.status}"]]/div[2]'),
                'type': 'text', 'param': {'up': 'Up', 'down': 'Down'}}),
            ('description', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.description}"]]/div[2]'),
                'type': 'text'}),
            ('connection_time', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.connection_time}"]]/div[2]'),
                'type': 'text', 'param': {'day': self.locale.day}}),
        ]

    @property
    def lan_locators(self) -> list:
        return [
            ('ip_address', {'locator': self.page.locator('#primary_ip'), 'type': 'text'}),
            ('netmask', {'locator': self.page.locator('#netmask'), 'type': 'text'}),
            ('description', {'locator': self.page.locator('#description'), 'type': 'text'}),
            ('shutdown', {'locator': self.page.locator('#shutdown'), 'type': 'switch_button'}),
            ('secondary_ip_settings', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('secondary_ip', {'locator': self.page.locator('#secondary_ip'), 'type': 'text'}),
                    ('netmask',
                     {'locator': self.page.locator('.ant-modal-content').locator('#netmask'), 'type': 'text'}),
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
