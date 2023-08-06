# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 14:19:19
# @Author  : Pane Li
# @File    : routing_status_locators.py
"""
routing_status_locators

"""
from playwright.sync_api import Page


class RoutingStatusLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def routing_locators(self) -> list:
        return [
            ('routing_type', {'locator': self.page.locator('.ant-select.ant-select-enabled'), 'type': 'select',
                              'param': {'all': self.locale.all, 'connected_routing': self.locale.connected_routing,
                                        'static_routing': self.locale.static_routing, 'ospf': 'OSPF', 'bgp': 'BGP',
                                        'rip': 'RIP'}}),
        ]

    @property
    def routing_table_locators(self) -> dict:
        return {'locator': self.page.locator(
            '.ant-table.ant-table-default.ant-table-bordered.ant-table-scroll-position-left'),
            'type': 'table_tr',
            'param': {'all': self.locale.all, 'connected_routing': self.locale.connected_routing,
                      'static_routing': self.locale.static_routing, 'ospf': 'OSPF', 'bgp': 'BGP',
                      'rip': 'RIP'}}
