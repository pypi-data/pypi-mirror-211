# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 9:57:14
# @Author  : Pane Li
# @File    : wlan_locators.py
"""
wlan_locators

"""
from playwright.sync_api import Page


class WlanLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def wlan_status_locators(self) -> list:
        return [
            ('station_role', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.station_role}"]]/div[2]'),
                'type': 'text', 'param': {'ap': self.locale.ap, 'client': self.locale.client}}),
            ('wlan_status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.wlan_status}"]]/div[2]'),
                'type': 'text', 'param': {'enable': self.locale.enable, 'disable': self.locale.disable}}),
            ('mac_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.mac_address}"]]/div[2]'),
                'type': 'text'}),
            ('ssid', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="SSID"]]/div[2]'),
                'type': 'text'}),
            ('channel', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.channel}"]]/div[2]'),
                'type': 'text'}),
            ('auth_method', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.auth_method}"]]/div[2]'),
                'type': 'text', 'param': {'OPEN': self.locale.open.upper(), 'SHARED': self.locale.shared.upper()}}),
            ('encrypt_mode', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.encrypt_mode}"]]/div[2]'),
                'type': 'text'}),
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
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="DNS"]]/div[2]'),
                'type': 'text'}),
            ('wireless_connection_status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.wireless_connection_status}"]]/div[2]'),
                'type': 'text', 'param': {'disconnect': self.locale.disconnect, 'connect': self.locale.connect}}),
            ('connection_time', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.connection_time}"]]/div[2]'),
                'type': 'text', 'param': {'day': self.locale.day}}),

        ]

    @property
    def wlan_locators(self) -> list:
        return [
            ('enable_wifi', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('station_role', {'locator': self.page.locator('#station_role'), 'type': 'radio_select',
                              'param': {'ap': self.locale.ap, 'client': self.locale.client},
                              'relation': [('enable_wifi', 'enable')]}),
            ('sta_default_route', {'locator': self.page.locator('#sta_default_route'), 'type': 'switch_button',
                                   'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_ssid', {'locator': self.page.locator('#sta_ssid'), 'type': 'text',
                          'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_scan', {'locator': self.page.locator(f'//button[@type="button"]/span[text()="{self.locale.scan}"]'),
                          'type': 'button', 'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_connect',
             {'locator': {"locator": self.page.locator('.antd-pro-components-in-gateway-network-profile-outerBox'),
                          }, 'type': 'table_tr', 'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_auth_method', {'locator': self.page.locator('#sta_auth_method'), 'type': 'select',
                                 'param': {'OPEN': self.locale.open.upper(), 'SHARED': self.locale.shared.upper()},
                                 'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_encrypt_mode', {'locator': self.page.locator('#sta_encrypt_mode'), 'type': 'select',
                                  'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_wep_key', {'locator': self.page.locator('#sta_wep_key'), 'type': 'text',
                             'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_wpa_psk_key', {'locator': self.page.locator('#sta_wpa_psk_key'), 'type': 'text',
                                 'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_auth_mode', {'locator': self.page.locator('#sta_auth_mode'), 'type': 'radio_select',
                               'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_inner_auth', {'locator': self.page.locator('#sta_inner_auth'), 'type': 'radio_select',
                                'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_username', {'locator': self.page.locator('#sta_username'), 'type': 'text',
                              'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_password', {'locator': self.page.locator('#sta_password'), 'type': 'text',
                              'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_network_type', {'locator': self.page.locator('#sta_dhcp'), 'type': 'radio_select',
                                  'param': {'static_ip': self.locale.static_ip,
                                            'dynamic_address_dhcp': self.locale.dynamic_address_dhcp},
                                  'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_ip_address', {'locator': self.page.locator('#ip_addr'), 'type': 'text'}),
            ('sta_netmask', {'locator': self.page.locator('#netmask'), 'type': 'text'}),
            ('ap_ssid_broadcast', {'locator': self.page.locator('#ap_ssid_broadcast'), 'type': 'switch_button',
                                   'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_bridge', {'locator': self.page.locator('#ap_briage'), 'type': 'switch_button',
                           'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_band', {'locator': self.page.locator('#ap_band'), 'type': 'select',
                         'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_radio_type', {'locator': self.page.locator('#ap_radio_type'), 'type': 'select',
                               'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_channel', {'locator': self.page.locator('#ap_channel'), 'type': 'select',
                            'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_ssid', {'locator': self.page.locator('#ap_ssid'), 'type': 'text',
                         'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_auth_method', {'locator': self.page.locator('#auth_method'), 'type': 'select',
                                'param': {'OPEN': self.locale.open.upper(), 'SHARED': self.locale.shared.upper()},
                                'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_encrypt_mode', {'locator': self.page.locator('#encrypt_mode'), 'type': 'select',
                                 'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_wep_key', {'locator': self.page.locator('#wep_key'), 'type': 'text',
                            'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_wpa_psk_key', {'locator': self.page.locator('#wpa_psk_key'), 'type': 'text',
                                'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_bandwidth', {'locator': self.page.locator('#ap_bandwidth'), 'type': 'select',
                              'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_stations_limit', {'locator': self.page.locator('#ap_max_associations'), 'type': 'text',
                                   'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'text_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]
