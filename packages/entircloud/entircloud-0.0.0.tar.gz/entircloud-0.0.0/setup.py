#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2023 Thomas Harr <xDevThomas@gmail.com>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2023-05-29
#

from setuptools import setup

name = 'entircloud'
author = 'Thomas Harr'
author_email = 'xDevThomas@gmail.com'
url = 'https://entir.io'
description = 'This library allows connecting to the self-hosted IoT messaging and device management cloud platform written in Go'
keywords = 'iot, smart-home, cloud, wifi, ble, control, sensors, smartphone, mobile, ota, self-hosted'
packages = []
package_data = {}
classifiers = ['Development Status :: 1 - Planning']

setup(
    name=name,
    version='0.0.0',
    description=description,
    long_description='',
    url=url,
    author=author,
    author_email=author_email,
    packages=packages,
    classifiers=classifiers,
)
