# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 15:35:23
# @Author  : Pane Li
# @File    : nat_locators.py
"""
nat_locators

"""
from playwright.sync_api import Page


class NatLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def nat_locators(self) -> list:
        return [
            ('nat_rules',
             {'locator': {
                 'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox').nth(0),
                 "columns": [
                     ('action', {'locator': self.pop_up.locator('#action'), 'type': 'select'}),
                     ('source_network', {'locator': self.pop_up.locator('#source_network'), 'type': 'radio_select',
                                         'param': {'inside': self.locale.inside, 'outside': self.locale.outside}}),
                     ('translation_type', {'locator': self.pop_up.locator('#translation_type'), 'type': 'select'}),
                     ('virtual_ip',
                      {'locator': self.pop_up.locator('//input[@id="transmit_source.ip_addr"]'), 'type': 'text'}),
                     ('interface',
                      {'locator': self.pop_up.locator('//input[@id="transmit_dest.interface"]'), 'type': 'select'}),
                     ('real_ip',
                      {'locator': self.pop_up.locator('//input[@id="transmit_dest.ip_addr"]'), 'type': 'text'}),
                     ('source_ip',
                      {'locator': self.pop_up.locator('//input[@id="source_range.ip_addr"]'), 'type': 'text'}),
                     ('source_netmask',
                      {'locator': self.pop_up.locator('//input[@id="source_range.netmask"]'), 'type': 'text'}),
                     ('transmit_protocol',
                      {'locator': self.pop_up.locator('#transmit_protocol'), 'type': 'radio_select'}),
                     ('match_ip',
                      {'locator': self.pop_up.locator('//input[@id="transmit_source.ip_addr"]'), 'type': 'text'}),
                     ('match_interface',
                      {'locator': self.pop_up.locator('//div[@id="transmit_source.interface"]'), 'type': 'select'}),
                     ('match_port',
                      {'locator': self.pop_up.locator('//input[@id="transmit_source.port"]'), 'type': 'text'}),
                     ('match_end_port',
                      {'locator': self.pop_up.locator('//input[@id="transmit_source.end_port"]'), 'type': 'text'}),
                     ('match_acl',
                      {'locator': self.pop_up.locator('//div[@id="transmit_source.acl_num"]'), 'type': 'select'}),
                     ('translated_ip',
                      {'locator': self.pop_up.locator('//input[@id="transmit_dest.ip_addr"]'), 'type': 'text'}),
                     ('translated_interface',
                      {'locator': self.pop_up.locator('//div[@id="transmit_dest.interface"]'), 'type': 'select'}),
                     ('translated_port',
                      {'locator': self.pop_up.locator('//input[@id="transmit_dest.port"]'), 'type': 'text'}),
                     ('translated_end_port',
                      {'locator': self.pop_up.locator('//input[@id="transmit_dest.end_port"]'), 'type': 'text'}),
                     ('log', {'locator': self.pop_up.locator('#log'), 'type': 'switch_button'}),
                     ('description', {'locator': self.pop_up.locator('#description'), 'type': 'text'}),
                     ('errors_text', {'type': 'text_messages'}),
                     ('cancel',
                      {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                       'type': 'button'}),
                     ('save',
                      {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'),
                       'type': 'button'})]},
                 'type': 'table_tr', 'param': {'inside': self.locale.inside, 'outside': self.locale.outside}}),
            ('network_interface',
             {'locator': {
                 'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox').nth(1),
                 "columns": [
                     ('interface', {'locator': self.page.locator('#interface'), 'type': 'select'}),
                     ('interface_type',
                      {'locator': self.pop_up.locator('#type'), 'type': 'radio_select',
                       'param': {'inside': self.locale.inside, 'outside': self.locale.outside}}),
                     ('errors_text', {'type': 'text_messages'}),
                     ('cancel',
                      {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                       'type': 'button'}),
                     ('save',
                      {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'),
                       'type': 'button'})]},
                 'type': 'table_tr', 'param': {'inside': self.locale.inside, 'outside': self.locale.outside}}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]
