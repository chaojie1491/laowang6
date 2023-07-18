import hashlib
import os
import shutil
import uuid
from datetime import datetime
import urllib

import pandas as pd
import sqlite3

import requests


conn = sqlite3.connect(database='db.sqlite3')
cursor = conn.cursor()
domain = ''
'id, phone_number, identity_number, invitation_code, real_name, create_time, approval_status, approval_time, reject_reason, max_invitation_number, identity_photo_id'
df = pd.read_excel("20230718134542.xls")

UPLOAD_ROOT = '/opt/files/identity/'
UPLOAD_URL = '/upload/files/identity/'
def save_file_(file_obj,file_name):
    def get_unique_str():
        uuid_str = str(uuid.uuid4())
        md5 = hashlib.md5()
        md5.update(uuid_str.encode('utf-8'))
        return md5.hexdigest()

    if file_obj is None:
        raise Exception('文件不存在')
    else:

        filename = file_name
        filepath = os.path.join(UPLOAD_ROOT + file_name)

        file_net_path = UPLOAD_URL + file_name


    sql = f'''insert into blog_filerecord (origin_name, file_name, file_path, create_date, suffix, file_net_path) values ('{file_obj.name}','{filename}','{filepath}','2023-07-17 18:47:59','{file_obj.name.split('.')[-1]}','{file_net_path}')
    '''
    print(sql)
    cursor.execute(sql)
    conn.commit()

    return cursor.lastrowid

def get_approval(status):
    if status == '已审核':
        return 1
    elif status == '待审核':
        return 3
    else:
        return 2
def download_and_save_file(item):
    if get_approval(item[8]) == 1:
        if item[9] is not None or item[9] != '':
            url = domain + item[9]
            r = requests.get(url)
            file_save_path =  UPLOAD_ROOT + item[9][item[9].rindex('/') + 1:]
            with open(file_save_path, "wb") as code:
                code.write(r.content)
            code.close()
            file = open(file_save_path)
            return save_file_(file,item[9][item[9].rindex('/') + 1:])
    else:
        return 'null'

for item in df.values:
    # sql.format(, item[1], item[2], item[3], item[5], datetime.strptime(item[6], '%Y-%m-%d %H:%M:%S'),
    #            get_approval(item[8]), datetime.strptime(item[7], '%Y-%m-%d %H:%M:%S'), item[8], 10,
    #            download_and_save_file(item)
    #            )

    search_sql = f"select * from blog_nuser where phone_number = '{item[1]}'"
    fetchall = cursor.execute(search_sql).fetchall()
    if len(fetchall) == 0:
        sql = f"insert into blog_nuser (id, phone_number,password, real_name, identity_number, invitation_code, create_time, " \
              f"approval_status, approval_time, reject_reason, max_invitation_number, identity_photo_id ,status) " \
              f"values ({item[0]},'{item[1]}','123456','{item[2]}','{item[3]}','{item[5]}','{datetime.strptime(item[6], '%Y-%m-%d %H:%M:%S')}'," \
              f"'{get_approval(item[8])}','{datetime.strptime(item[7], '%Y-%m-%d %H:%M:%S')}','{item[8]}',10,{download_and_save_file(item)},1)"

        print(sql)

        cursor.execute(sql)
    else:
        print(f'{item[1]}已经存在')
    conn.commit()
