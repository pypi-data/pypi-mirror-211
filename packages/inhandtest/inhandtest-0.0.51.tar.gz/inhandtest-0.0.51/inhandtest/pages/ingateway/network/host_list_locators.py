# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 16:42:04
# @Author  : Pane Li
# @File    : host_list_locators.py
"""
host_list_locators

"""
from playwright.sync_api import Page


class HostListLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def hostlist_status_locators(self) -> dict:
        return {"locator": self.page.locator('.ant-table-scroll-position-left')}
