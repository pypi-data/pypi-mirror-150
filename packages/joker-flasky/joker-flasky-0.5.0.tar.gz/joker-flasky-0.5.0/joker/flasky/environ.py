#!/usr/bin/env python3
# coding: utf-8

"""
For internal use within `joker-flasky`.
"""

from functools import cached_property

import volkanic


class JokerInterface(volkanic.GlobalInterface):
    package_name = 'joker.flasky'

    @cached_property
    def jinja2_env(self):
        # noinspection PyPackageRequirements
        from jinja2 import Environment, PackageLoader, select_autoescape
        return Environment(
            loader=PackageLoader(self.package_name, 'templates'),
            autoescape=select_autoescape(['html', 'xml']),
            **self.conf.get('_jinja2_env', {})
        )
