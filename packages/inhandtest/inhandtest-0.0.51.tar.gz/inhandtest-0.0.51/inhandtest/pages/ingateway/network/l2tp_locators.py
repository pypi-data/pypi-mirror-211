# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 11:05:32
# @Author  : Pane Li
# @File    : l2tp_locators.py
"""
l2tp_locators

"""
from playwright.sync_api import Page


class L2tpLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def l2tp_client_status_locators(self) -> dict:
        return {'locator': self.page.locator(
            '.ant-table.ant-table-default.ant-table-bordered.ant-table-empty.ant-table-scroll-position-left').nth(0),
                'type': 'table_tr',
                'param': {'disconnect': self.locale.disconnect, 'connect': self.locale.connect,
                          'disable': self.locale.disable}}

    @property
    def l2tp_server_status_locators(self) -> dict:
        return {'locator': self.page.locator(
            '.ant-table.ant-table-default.ant-table-bordered.ant-table-empty.ant-table-scroll-position-left').nth(1),
                'type': 'table_tr',
                'param': {'disconnect': self.locale.disconnect, 'connect': self.locale.connect,
                          'disable': self.locale.disable}}

    @property
    def l2tp_client_locators(self) -> list:
        return [
            ('l2tp_class', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-tableBox').nth(0),
                "columns": [
                    ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                    ('auth', {'locator': self.pop_up.locator('#authentication'), 'type': 'radio_select',
                              'param': {'yes': self.locale.yes, 'no': self.locale.no}}),
                    ('hostname', {'locator': self.pop_up.locator('#hostname'), 'type': 'text'}),
                    ('challenge_secret', {'locator': self.pop_up.locator('#challenge_secret'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr',
                'param': {'yes': self.locale.yes, 'no': self.locale.no}}),
            ('pseudowire_class', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-tableBox').nth(1),
                "columns": [
                    ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                    ('l2tp_class', {'locator': self.pop_up.locator('#class'), 'type': 'select'}),
                    ('source_interface', {'locator': self.pop_up.locator('#source_interface'), 'type': 'select'}),
                    ('data_encapsulation_method',
                     {'locator': self.pop_up.locator('#data_encapsulation_method'), 'type': 'select'}),
                    ('tunnel_management_protocol',
                     {'locator': self.pop_up.locator('#tunnel_management_protocol'), 'type': 'select'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr'}),
            ('l2tpv2_tunnel', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-tableBox').nth(2),
                "columns": [
                    ('enable', {'locator': self.pop_up.locator('#enable'), 'type': 'switch_button'}),
                    ('id', {'locator': self.pop_up.locator('#id'), 'type': 'text'}),
                    ('l2tp_server', {'locator': self.pop_up.locator('#server'), 'type': 'text'}),
                    ('pseudowire_class', {'locator': self.pop_up.locator('#pseudowire_class'), 'type': 'select'}),
                    ('auth_type', {'locator': self.pop_up.locator('#authentication_type'), 'type': 'select',
                                   'param': {'AUTO': self.locale.auto}}),
                    ('username', {'locator': self.pop_up.locator('#username'), 'type': 'text'}),
                    ('password', {'locator': self.pop_up.locator('#password'), 'type': 'text'}),
                    ('local_ip_address', {'locator': self.pop_up.locator('#local_ip_address'), 'type': 'text'}),
                    ('remote_ip_address', {'locator': self.pop_up.locator('#remote_ip_address'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr'}),
            ('l2tpv3_tunnel', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-tableBox').nth(3),
                "columns": [
                    ('enable', {'locator': self.pop_up.locator('#enable'), 'type': 'switch_button'}),
                    ('id', {'locator': self.pop_up.locator('#id'), 'type': 'text'}),
                    ('peer_id', {'locator': self.pop_up.locator('#peer_id'), 'type': 'text'}),
                    ('pseudowire_class', {'locator': self.pop_up.locator('#pseudowire_class'), 'type': 'select'}),
                    ('protocol', {'locator': self.pop_up.locator('#protocol'), 'type': 'select'}),
                    ('source_port', {'locator': self.pop_up.locator('#source_port'), 'type': 'text'}),
                    ('destination_port', {'locator': self.pop_up.locator('#destination_port'), 'type': 'text'}),
                    ('xconnect_interface', {'locator': self.pop_up.locator('#xconnect_interface'), 'type': 'select'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr'}),
            ('l2tpv3_session', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-tableBox').nth(4),
                "columns": [
                    ('local_session_id', {'locator': self.pop_up.locator('#local_session_id'), 'type': 'text'}),
                    ('remote_session_id', {'locator': self.pop_up.locator('#remote_session_id'), 'type': 'text'}),
                    ('local_tunnel_id', {'locator': self.pop_up.locator('#local_tunnel_id'), 'type': 'select'}),
                    ('local_session_ip_address',
                     {'locator': self.pop_up.locator('#local_session_ip_address'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button'}),
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

    @property
    def l2tp_service_locators(self) -> list:
        return [
            ('enable', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('username', {'locator': self.page.locator('#username'), 'type': 'text', 'relation': [('enable', True)]}),
            ('password', {'locator': self.page.locator('#password'), 'type': 'text', 'relation': [('enable', True)]}),
            ('auth_type',
             {'locator': self.page.locator('#authentication_type'), 'type': 'select', 'relation': [('enable', True)],
              'param': {'AUTO': self.locale.auto}}),
            ('local_ip_address',
             {'locator': self.page.locator('#local_ip_address'), 'type': 'text', 'relation': [('enable', True)]}),
            ('client_start_ip',
             {'locator': self.page.locator('#client_start_ip_address'), 'type': 'text',
              'relation': [('enable', True)]}),
            ('client_end_ip',
             {'locator': self.page.locator('#client_end_ip_address'), 'type': 'text', 'relation': [('enable', True)]}),
            ('link_detection_interval', {'locator': self.page.locator('#link_detection_interval'), 'type': 'text',
                                         'relation': [('enable', True)]}),
            ('max_retries_for_link', {'locator': self.page.locator('#max_retries_for_link'), 'type': 'text',
                                      'relation': [('enable', True)]}),
            ('enable_mppe', {'locator': self.page.locator('#enable_mppe'), 'type': 'switch_button'}),
            ('enable_tunnel_auth',
             {'locator': self.page.locator('#enable_tunnel_authentication'), 'type': 'switch_button'}),
            ('challenge_secrets', {'locator': self.page.locator('#challenge_secrets'), 'type': 'text',
                                   'relation': [('enable', True), ('enable_tunnel_auth', True)]}),
            ('server_name', {'locator': self.page.locator('#server_name'), 'type': 'text',
                             'relation': [('enable', True), ('enable_tunnel_auth', True)]}),
            ('client_name', {'locator': self.page.locator('#client_name'), 'type': 'text',
                             'relation': [('enable', True), ('enable_tunnel_auth', True)]}),
            ('export_options',
             {'locator': self.page.locator('#export_options'), 'type': 'text', 'relation': [('enable', True)]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]
