# -*- coding: UTF-8 -*-
# @Time : 2022/5/11 下午4:06 
# @Author : 刘洪波


def load_config(config_path: str, is_linux=True):
    from filebeat.Run import Filebeat
    return Filebeat(config_path, is_linux)
