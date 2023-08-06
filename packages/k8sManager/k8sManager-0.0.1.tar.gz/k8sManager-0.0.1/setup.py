'''
Author: ronnyrzyang
Date: 2023-05-25 11:55:14
LastEditors: ronnyrzyang@tencent.com
LastEditTime: 2023-05-31 10:33:41
FilePath: /ronnyrzyang/upload_pypi/ronnytest_for_py3/setup.py
Description: 
Copyright 2023 Tencent Inc.  All rights reserved
'''
from setuptools import setup,find_packages


def _permission_check(setup):

    # 面向内部用户文案
    def _in_check_actions():
        print('\033[91m*************************************************************************************************************************************\033[0m')
        print('\033[91m*************************************************************************************************************************************\033[0m')
        print("\033[91m[Warning]The package cannot be downloaded, please specify to use the company's internal source in the command or script to install package, for example : pip install --index-url=xxxx (tips from wxpsec)\033[0m")
        print('\033[91m*************************************************************************************************************************************\033[0m')
        print('\033[91m*************************************************************************************************************************************\033[0m')
        raise RuntimeError('do not install!')
    
    _in_check_actions()


setup(
    name = 'k8sManager',
    version = '0.0.1',
    author = 'wxpay_sec_team',
    author_email = 'wxpay_sec_team@tencent.com',
    packages = find_packages(),
    install_requires=[""],
    tests_require=[],
)

_permission_check(setup)