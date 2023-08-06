# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 15:58:25
# @Author  : Pane Li
# @File    : edge_computing_locators.py
"""
edge_computing_locators

"""
from inhandtest.pages.ingateway.edge_computing.docker_manager_locators import DockerManagerLocators
from inhandtest.pages.ingateway.edge_computing.python_edge_computing_locators import PythonEdgeComputingLocators


class EdgeComputingLocators(PythonEdgeComputingLocators, DockerManagerLocators):
    pass
