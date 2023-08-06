#!/usr/bin/env python3
# coding: utf-8

from joker.flasky.environ import JokerInterface

ji = JokerInterface()


def respond_login_page(
        username='', password='', title='Login') -> str:
    tpl = ji.jinja2_env.get_template('login.html')
    return tpl.render(
        username=username,
        password=password,
        title=title,
    )


def respond_upload_page(
        label='Choose a file to upload', title='Upload') -> str:
    tpl = ji.jinja2_env.get_template('upload.html')
    return tpl.render(label=label, title=title)
