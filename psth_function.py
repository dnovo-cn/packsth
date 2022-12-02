import json
import os
import shutil
import zipfile
import hashlib
import time
import uuid
from typing import Any
import globalData as gl


# 1.配置文件相关
# 判断当前目录下有无配置文件config.json，有则下一步无则创建
# 读取配置文件内容，为空初始化后进入配置填写并记录保存后下一步，不为空下一步
# 获取配置文件对程序参数进行设置

# 初始化配置文件以及配置参数
# 判断用户磁盘数，只有单个盘的情况下选取单个盘，多个盘的情况下选取除C盘外容量最大的一个盘，或者用户指定盘

# 初始化配置文件
def handle_config(status, params):
    if status == 'init':
        config_json = {
            "file_path": "D:\\packsth\\file",
            "package_path": "D:\\packsth\\package",
            "WinARA_path": "",
        }
        gl.set_value('config_json', config_json)
        with open('./config.json', 'w') as config:
            json.dump(config_json, config)
    else:
        with open("./config.json", 'r') as config_json:
            temp_json = json.loads(config_json.read())
            temp_json.update(params)
        gl.set_value('config_json', temp_json)
        with open('./config.json', 'w') as config:
            json.dump(temp_json, config)


# 初始化索引文件
def handle_indexes(status, params):
    if status == 'init':
        indexes_json = {
            "fileList": [],
            "author": "",
            "create_date": "",
            "edit_date": ""
        }
        gl.set_value('indexes_json', indexes_json)
        with open('./indexes.json', 'w') as indexes:
            json.dump(indexes_json, indexes)
    else:
        with open("./indexes.json", 'r') as indexes_json:
            temp_json = json.loads(indexes_json.read())
            temp_json.update(params)
        gl.set_value('indexes_json', temp_json)
        with open('./indexes.json', 'w') as indexes:
            json.dump(temp_json, indexes)


# 程序初始化
def app_init():
    # 检测配置文件
    if 'config.json' in os.listdir('.'):
        with open("./config.json", 'r') as config_json:
            gl.set_value('config_json', json.load(config_json))
            print(gl.get_value('config_json'))
    else:
        handle_config('init', '')
    # 检测索引文件-
    if 'indexes.json' in os.listdir('.'):
        with open("./indexes.json", 'r') as indexes_json:
            gl.set_value('indexes_json', json.load(indexes_json))
            print(gl.get_value('indexes_json'))
    else:
        handle_indexes('init', '')


# 文件处理
def handle_file():
    file_list = os.listdir(gl.get_value('config_json').get('file_path'))
    if len(gl.get_value('indexes_json').get('fileList')):
        begin_id = gl.get_value('indexes_json').get('fileList')[-1].get('file_id')
    else:
        begin_id = 1
    gl.set_value('queue_num', len(file_list))
    for inx, val in enumerate(file_list):
        cur_id = begin_id + inx
        handle_file_info(cur_id, val)


# 文件索引表处理
def handle_file_info(file_id, file_name):
    current_path: str | Any = add_common_file(gl.get_value('config_json').get('file_path') + '/' + file_name)
    path, filename = os.path.split(current_path)
    current_file_size = get_dir_size(current_path)
    pack_suffix = '.zip'
    _file_name = filename_format(1, file_id)
    pack_name = _file_name + pack_suffix
    file_info = {
        "file_id": file_id,
        "file_name": filename,
        "file_source": "",
        "file_size": current_file_size,
        "file_type": "",
        "file_tag": "",
        "file_remark": "",
        "file_encryption": False,
        "encrypt_key": "",
        "pack_name": _file_name,
        "pack_suffix": pack_suffix,
        "pack_size": "",
        "save_pos": "cloud",
        "cloud_type": "bd",
    }
    gl.get_value('indexes_json').get('fileList').append(file_info)
    if gl.get_value('config_json').get('package_path'):
        zip_path = gl.get_value('config_json').get('package_path') + '/' + pack_name
    else:
        zip_path = gl.get_value('config_json').get('file_path') + '/' + pack_name
    file2package(current_path, zip_path, file_id)


# 保存文件索引表
def save_filelist_json(content):
    with open('./filelist.json', 'w') as filelist:
        json.dump(content, filelist)


# 获取文件夹大小
def get_dir_size(_dir, size=0):
    if os.path.isfile(_dir):
        size = os.path.getsize(_dir)
    else:
        for root, dirs, files in os.walk(_dir):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    for count in ['Bytes', 'KB', 'MB', 'GB']:
        if -1024.0 < size < 1024.0:
            return "%3.1f%s" % (size, count)
        size /= 1024.0
    return "%3.1f%s" % (size, 'TB')


# 压缩文件
def file2package(file_path, zip_path, file_id):
    # 调用winARA程序进行加密压缩
    winrar_path = gl.get_value('config_json').get('WinARA_path')
    if winrar_path:
        password = "ovo123ovo"
        winrar_path = gl.get_value('config_json').get('WinARA_path')
        # 1G分卷  -v1024000 去除路径 -ep1 压缩密码 -p 清除源文件 -dw 屏蔽所有消息 -inul
        cmd = r'' + winrar_path + ' a -v1024000 -ep1 -p%s %s %s' % (password, zip_path, file_path)
        result = os.system(cmd)  # 执行压缩命令
        if result == 0:
            temp_info = gl.get_value('indexes_json').get('fileList')
            temp = {
                "file_encryption": True,
                "encrypt_key": password,
                "pack_size": get_dir_size(zip_path),
            }
            for info in temp_info:
                if info['file_id'] == file_id:
                    info.update(temp)
            queue_num = gl.get_value('queue_num') - 1
            if not queue_num:
                time.sleep(3)
                handle_indexes('update', gl.get_value('indexes_json'))
            gl.set_value('queue_num', queue_num)
        else:
            print('FAILED Compress', file_path)
    else:
        # 使用zipfile插件进行非加密的z包压缩
        zipf = zipfile.ZipFile(zip_path, 'w')
        pre_len = len(os.path.dirname(file_path))
        for parent, _, filenames in os.walk(file_path):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                zipf.write(pathfile, arcname)
        zipf.close()
        temp_info = gl.get_value('indexes_json').get('fileList')
        temp = {
            "pack_size": get_dir_size(zip_path),
        }
        for info in temp_info:
            if info['file_id'] == file_id:
                info.update(temp)
        queue_num = gl.get_value('queue_num') - 1
        if not queue_num:
            time.sleep(3)
            handle_indexes('update', gl.get_value('indexes_json'))
        gl.set_value('queue_num', queue_num)




# 修改文件后缀名防止在线解压
# def change_suffix():


# 添加无意义或自定义文件，避免MD5记录值重复被和谐-对单文件数据进行文件夹包裹
def add_common_file(_path):
    if os.path.isdir(_path):
        file = open(_path + '/README.txt', 'w')
        file.write(str(uuid.uuid1()))
    else:
        path, filename = os.path.split(_path)
        dir_path = path + '/' + filename.split('.')[0]
        os.makedirs(dir_path)
        shutil.move(_path, dir_path)
        file = open(dir_path + '/README.txt', 'w')
        file.write(str(uuid.uuid1()))
        _path = dir_path
    return _path


def get_md5(pws):
    md5 = hashlib.md5()
    md5.update(pws.encode('utf-8'))
    return md5.hexdigest()


def filename_format(status, param):
    if status == 1:
        prefix = 'PSth_1o24_'
        cur_time = int(time.time())
        cur_id = str(param)
        if len(cur_id) < 5:
            for i in range(5 - len(str(param))):
                cur_id = '0' + cur_id
        temp_filename = prefix + str(cur_time) + '_' + cur_id
    elif status == 2:
        temp_filename = get_md5(param)
    else:
        temp_filename = param
    return temp_filename

# handle_file()

# 2.文件处理相关
# 用户指定目录，选则单个处理或批量处理，并设置参数
# 按照参数执行相应操作
# 读取文件，创建文本并开始记录
