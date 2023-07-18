#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django import template
from django.utils.html import format_html
from datetime import datetime
from django import template

# 注册标签
register = template.Library()


@register.simple_tag
def circle_page(curr_page, loop_page):
    curr_page = int(curr_page)
    loop_page = int(loop_page)
    offset = abs(curr_page - loop_page)
    if offset < 3:
        if curr_page == loop_page:
            page_ele = ' <a class="item active" href="?page=%s">%s</a> ' % (
                loop_page, loop_page)
        else:
            page_ele = ' <a class="item" href="?page=%s">%s</a>' % (loop_page, loop_page)
        return format_html(page_ele)
    else:
        return ''


@register.simple_tag
def circle_page_index(curr_page, loop_page):
    curr_page = int(curr_page)
    loop_page = int(loop_page)
    offset = abs(curr_page - loop_page)
    if offset < 3:
        if curr_page == loop_page:
            page_ele = ' <li><a href="?page=%s" aria-current="page"><span class="visuallyhidden">page </span>%s</a></li>' % (
                loop_page, loop_page)
        else:
            page_ele = '  <li><a  href="?page=%s"><span class="visuallyhidden">page </span>%s</a></li>' % (
            loop_page, loop_page)
        return format_html(page_ele)
    else:
        return ''

@register.simple_tag
def circle_page_index_z(curr_page, loop_page):
    curr_page = int(curr_page)
    loop_page = int(loop_page)
    offset = abs(curr_page - loop_page)
    if offset < 3:
        if curr_page == loop_page:
            page_ele = '<li class="active"><a  href="?page=%s">%s</a></li>' % (
                loop_page, loop_page)
        else:
            page_ele = '<li  ><a  href="?page=%s" class="active">%s</a></li>' % (
            loop_page, loop_page)
        return format_html(page_ele)
    else:
        return ''

