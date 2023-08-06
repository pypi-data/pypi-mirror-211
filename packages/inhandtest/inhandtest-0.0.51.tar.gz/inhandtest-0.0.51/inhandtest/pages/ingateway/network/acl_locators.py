# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 15:35:11
# @Author  : Pane Li
# @File    : acl_locators.py
"""
acl_locators

"""
from playwright.sync_api import Page


class AclLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def acl_locators(self) -> list:
        common = self.pop_up.locator('.ant-select.ant-select-enabled')
        return [
            ('default_filter_strategy',
             {'locator': self.page.locator('#default_policy'), 'type': 'radio_select',
              'param': {'permit': self.locale.permit, 'deny': self.locale.deny}}),
            ('access_control_strategy',
             {'locator': {
                 'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                 "columns": [
                     ('acl_type', {'locator': self.pop_up.locator('#acl_type'), 'type': 'radio_select',
                                   'param': {'standard': self.locale.standard, 'extended': self.locale.extended}}),
                     ('id', {'locator': self.pop_up.locator('#id'), 'type': 'text'}),
                     ('sequence_number', {'locator': self.pop_up.locator('#sequence_number'), 'type': 'text'}),
                     ('action', {'locator': self.pop_up.locator('#action'), 'type': 'radio_select',
                                 'param': {'permit': self.locale.permit, 'deny': self.locale.deny}}),
                     ('protocol', {'locator': common.nth(0), 'type': 'select'}),
                     ('protocol_id', {'locator': common.nth(0).locator('../div[2]').locator(
                         '//input[@role="spinbutton"]'), 'type': 'text'}),
                     ('source_ip', {'locator': self.pop_up.locator('//input[@id="acl_source.ip"]'), 'type': 'text'}),
                     ('source_wildcard',
                      {'locator': self.pop_up.locator('//input[@id="acl_source.wildcard_mask"]'), 'type': 'text'}),
                     ('source_port', {'locator': common.nth(1), 'type': 'select'}),
                     ('source_port_value', {'locator': common.nth(1).locator('../div[2]').locator(
                         '//input[@role="spinbutton"]'), 'type': 'text'}),
                     ('source_port_value1', {'locator': common.nth(1).locator('../div[3]').locator(
                         '//input[@role="spinbutton"]'), 'type': 'text'}),
                     ('destination_ip',
                      {'locator': self.pop_up.locator('//input[@id="acl_destination.ip"]'), 'type': 'text'}),
                     ('destination_wildcard',
                      {'locator': self.pop_up.locator('//input[@id="acl_destination.wildcard_mask"]'),
                       'type': 'text'}),
                     ('destination_port', {'locator': common.nth(2), 'type': 'select'}),
                     ('destination_port_value', {'locator': common.nth(2).locator('../div[2]').locator(
                         '//input[@role="spinbutton"]'), 'type': 'text'}),
                     ('destination_port_value1', {'locator': common.nth(2).locator('../div[3]').locator(
                         '//input[@role="spinbutton"]'), 'type': 'text'}),
                     ('icmp_type', {'locator': self.page.locator('#icmp_type'), 'type': 'radio_select',
                                    'param': {'used_describe': self.locale.used_describe,
                                              'use_type_code': self.locale.use_type_code}}),
                     ('icmp_describe', {'locator': self.page.locator('#icmp_describe_value'), 'type': 'select'}),
                     ('icmp_type_value', {'locator': self.page.locator('#icmp_code_value'), 'type': 'text'}),
                     ('icmp_code', {'locator': self.page.locator('#icmp_type_value'), 'type': 'text'}),
                     ('fragments', {'locator': self.page.locator('.ant-modal-content').locator('#fragments'),
                                    'type': 'switch_button'}),
                     ('established', {'locator': self.page.locator('.ant-modal-content').locator('#established'),
                                      'type': 'switch_button'}),
                     ('log', {'locator': self.page.locator('.ant-modal-content').locator('#log'),
                              'type': 'switch_button'}),
                     ('description', {'locator': self.page.locator('.ant-modal-content').locator('#description'),
                                      'type': 'text'}),
                     ('errors_text', {'type': 'text_messages'}),
                     ('cancel',
                      {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                       'type': 'button'}),
                     ('save',
                      {'locator': self.page.locator('.ant-modal-content').locator(
                          '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'})]},
                 'type': 'table_tr'}),
            ('access_control_list',
             {'locator': {
                 'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table-index-outerBox'),
                 "columns": [
                     ('interface', {'locator': self.page.locator('#interface'), 'type': 'select'}),
                     ('in_acl',
                      {'locator': self.page.locator('.ant-modal-content').locator('#inbound_acl'), 'type': 'select'}),
                     ('out_acl',
                      {'locator': self.page.locator('.ant-modal-content').locator('#outbound_acl'), 'type': 'select'}),
                     ('admin_acl',
                      {'locator': self.page.locator('.ant-modal-content').locator('#admin_acl'), 'type': 'select'}),
                     ('errors_text', {'type': 'text_messages'}),
                     ('success_tip', {'type': 'tip_messages'}),
                     ('cancel',
                      {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                       'type': 'button'}),
                     ('save',
                      {'locator': self.page.locator('.ant-modal-content').locator(
                          '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'})]},
                 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]
