# -*- coding: utf-8 -*-
# @Datetime : 2023/9/30 9:18
# @Author   : WANGKANG
# @Blog     : kang17.xyz
# @File     : main.py
# @brief    : 使用QT编写的数据标注软件，想让我干垃圾活是不可能的，这辈子都不可能的
# Copyright 2023 WANGKANG, All Rights Reserved.

'''
	真要命啊，写了300行代码不到，就快把自己绕晕了，真是无语
	现在看来，有必要学习一种好的软件架构，避免出现这种问题
	或者在编写软件之前，最好是西安思考下软件的结构
	就好比java springboot为什么很少有这种感觉，因为这种开发逻辑很死板，很固定，照着写就是了
	软件开发则不同
	好的软件结构真的能省很多时间的
	我这次就栽在软件结构上了
'''

import sys
from PyQt5.QtWidgets import QApplication
from utils.MyWindow import MainWindow

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
