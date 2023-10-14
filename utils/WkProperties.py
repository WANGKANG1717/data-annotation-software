# -*- coding: utf-8 -*-
# @Date     : 2023-10-14 13:54:19
# @Author   : WangKang
# @Blog     : kang17.xyz
# @Email    : 1686617586@qq.com
# @Filepath : WkProperties.py
# @Brief    : 解析properties
# Copyright 2023 WANGKANG, All Rights Reserved.

import os


class WkProperties:
    FILE_NOT_EXISTS = "文件不存在"
    INCORRECT_FORMAT = "格式有误"

    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.key_value = {}
        self.content = None  # 文件内容
        self.parse_data()

    def parse_data(self):
        if not os.path.exists(self.filepath):
            raise Exception(self.FILE_NOT_EXISTS)
        with open(self.filepath) as f:
            self.content = f.read()
        for line in self.content.split("\n"):
            line = line.strip().split("#")[0]  # 跳过注释
            if not line:
                continue
            if line.find("=") == -1:
                raise Exception(self.INCORRECT_FORMAT)
            data = line.split("=")
            key = data[0].strip()
            value = data[1].strip()
            self.key_value[key] = value

    def get(self, key):
        return self.key_value.get(key)

    def keys(self):
        return self.key_value.keys()

    def values(self):
        return self.key_value.values()