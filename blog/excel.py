from datetime import datetime

from openpyxl import Workbook

from system import settings
import pandas as pd


def nuser_excel(nusers):
    workbook = Workbook()

    def get_status(status):
        if status == 1:
            return "通过"
        elif status == 2:
            return "驳回"
        else:
            return "未审核"

    sheet = workbook.active
    sheet.title = '默认title'
    sheet.append(
        ['id', '手机号', '姓名', '身份证', '邀请码', '审核状态', '邀请总人数', '邀请人', '创建时间', '审批时间',
         '拒绝原因'])
    for data in nusers:
        sheet.append([
            data['id'],
            data['phone_number'],
            data['real_name'],
            data['identity_number'],
            data['invitation_code'],
            get_status(data['approval_status']),
            data['count'],
            data['invited_user__invitation_user__real_name'],
            datetime.strftime(data['create_time'], '%Y-%m-%d'),
            datetime.strftime(data['approval_time'], '%Y-%m-%d'),
            data['reject_reason']
        ])
    name =  settings.BASE_DIR.joinpath('用户列表.xlsx')
    workbook.save(name)
    return name
