# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 14:19:36
# @Author  : Pane Li
# @File    : static_routing_locators.py
"""
static_routing_locators

"""
from playwright.sync_api import Page


class StaticRoutingLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def static_routing_locators(self) -> list:
        return [
            ('routing',
             {'locator': {'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table-index-outerBox'),
                          "columns": [
                              ('destination', {'locator': self.page.locator('#destination'), 'type': 'text'}),
                              ('netmask',
                               {'locator': self.page.locator('.ant-modal-content').locator('#netmask'),
                                'type': 'text'}),
                              ('interface',
                               {'locator': self.page.locator('.ant-modal-content').locator('#interface'),
                                'type': 'select'}),
                              ('gateway',
                               {'locator': self.page.locator('.ant-modal-content').locator('#gateway'),
                                'type': 'text'}),
                              ('distance',
                               {'locator': self.page.locator('.ant-modal-content').locator('#distance'),
                                'type': 'text'}),
                              ('track_id',
                               {'locator': self.page.locator('.ant-modal-content').locator('#track'), 'type': 'text'}),
                              ('errors_text', {'type': 'text_messages'}),
                              ('cancel',
                               {'locator': self.page.locator('.ant-modal-content').locator(
                                   '//button[@class="ant-btn"]'),
                                   'type': 'button'}),
                              ('save',
                               {'locator': self.page.locator('.ant-modal-content').locator(
                                   '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'})]},
              'param': {'all': self.locale.all, 'connected_routing': self.locale.connected_routing,
                        'static_routing': self.locale.static_routing, 'ospf': 'OSPF', 'bgp': 'BGP',
                        'rip': 'RIP'}, 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]
