# -*- coding: UTF-8 -*-
# @Time : 2022/5/11 下午4:06 
# @Author : 刘洪波
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
this_file_path = os.path.realpath(__file__)
this_file_path_list = this_file_path.split('/')


class Filebeat(object):
    def __init__(self, file_path, is_linux):
        filebeat_name = 'filebeat-8.1.3-linux-x86_64' if is_linux else 'filebeat-8.1.3-darwin-x86_64'
        self.filebeat_path = f"{'/'.join(this_file_path_list[:-1])}/{filebeat_name}/"
        if not os.path.isfile(file_path):
            raise ValueError(f"{file_path} not exist!")
        else:
            shutil.copy(file_path, self.filebeat_path)
        self.pool = ThreadPoolExecutor(max_workers=2)

    def run(self):
        self.pool.submit(os.system, f"cd {self.filebeat_path}  && ./filebeat -e")
