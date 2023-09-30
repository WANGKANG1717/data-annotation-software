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

from PyQt5.QtWidgets import *
from mainwindow import Ui_mainWindow

import pandas as pd


class MainWindow(QMainWindow, Ui_mainWindow):
	UNANSWERABLE_REASON_MAP = {
		0: "understandability",
		1: "specificity",
		2: "contextual relevance",
		3: "factual consistency",
		4: "information sufficiency",
		5: "other"
	}
	# 无奈之下又做了一份反向映射，尴尬
	UNANSWERABLE_REASON_MAP2 = {
		"understandability": 0,
		"specificity": 1,
		"contextual relevance": 2,
		"factual consistency": 3,
		"information sufficiency": 4,
		"other": 5,
	}
	
	# 初始化ui
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		
		self.setupUi(self)
		self.init_signal()
		
		self.setWindowTitle('数据标注软件 By WANGKANG')
		self.setMinimumSize(800, 600)
		self.statusBar().showMessage('欢迎使用', 5000)  # 底部状态栏的提醒
		
		self.file_path = ''  # 文件路径
		self.excel_data = pd.DataFrame()  # 总的excel信息
		self.passage = ""  # 当前文章
		self.question = ""  # 当前问题
		self.data_size = -1  # 数据集大小
		self.current_index = 0  # 当前文章/问题下标
		self.answerable = True  # 问题是否可回答
		self.consistent = True  # 问题一致性 如果答案不可回答，则一致性为False
		
		self.disable_components()  # 一开始需要禁用按钮 等到打开文件后再开启按钮
	
	def disable_components(self):
		self.pushButton_next.setDisabled(True)
		self.pushButton_pre.setDisabled(True)
		self.radioButton_answerable.setDisabled(True)
		self.radioButton_unanswerable.setDisabled(True)
		self.comboBox_unanswerable_reason.setDisabled(True)
		self.lineEdit_unanswerable_notes.setDisabled(True)
		self.radioButton_consistent.setDisabled(True)
		self.radioButton_unconsistent.setDisabled(True)
		self.pushButton_notes_confirm.setDisabled(True)
	
	def enable_components(self):
		self.pushButton_next.setDisabled(False)
		self.pushButton_pre.setDisabled(False)
		self.radioButton_answerable.setDisabled(False)
		self.radioButton_unanswerable.setDisabled(False)
		self.comboBox_unanswerable_reason.setDisabled(False)
		self.lineEdit_unanswerable_notes.setDisabled(False)
		self.radioButton_consistent.setDisabled(False)
		self.radioButton_unconsistent.setDisabled(False)
		self.pushButton_notes_confirm.setDisabled(False)
	
	# 信号与槽的设置
	def init_signal(self):
		self.action_open.triggered.connect(self.open_file)
		self.pushButton_next.clicked.connect(self.next_passage_question)
		self.pushButton_pre.clicked.connect(self.pre_passage_question)
		self.radioButton_answerable.clicked.connect(lambda: self.set_answerable(True))
		self.radioButton_unanswerable.clicked.connect(lambda: self.set_answerable(False))
		self.radioButton_consistent.clicked.connect(lambda: self.set_consistent(True))
		self.radioButton_unconsistent.clicked.connect(lambda: self.set_consistent(False))
		self.comboBox_unanswerable_reason.currentIndexChanged.connect(self.change_unanswerable_reason)
		self.pushButton_notes_confirm.clicked.connect(self.set_notes)
		self.action_save.triggered.connect(self.save_file)
	
	def open_file(self):
		# print("open_file")
		path = QFileDialog.getOpenFileName(self, 'open')[0]
		if path:
			self.file_path = path
			self.excel_data = pd.read_excel(path)
			self.set_status_bar_msg("打开成功 " + path)
			self.init_component()
	
	def save_file(self):
		try:
			self.excel_data.to_excel(self.file_path, index=False)
			self.set_status_bar_msg("保存成功")
		except Exception as e:
			self.set_status_bar_msg("保存失败")
	
	def init_component(self):
		self.current_index = 0
		self.data_size = len(self.excel_data['passage'])
		self.enable_components()
		self.get_set_ui_from_source()
	
	def set_status_bar_msg(self, msg, timeout=5000):
		self.statusBar().showMessage(msg, timeout)
	
	def getPassage(self, current_index):
		self.passage = self.excel_data.loc[current_index, 'passage']
		# print(self.passage)
		self.textBrowser_passage.setText(self.passage)
	
	def getQuestion(self, current_index):
		self.question = self.excel_data.loc[current_index, 'target']
		# print(self.question)
		self.textBrowser_question.setText(self.question)
	
	def next_passage_question(self):
		# 这里首先要确保不可回答-其他 备注要填上
		if self.answerable == False:
			if not self.set_notes(self.comboBox_unanswerable_reason.currentIndex() == 5):
				return
		if self.current_index < self.data_size - 1:
			self.current_index += 1
			# 这里为了软件的通用性，需要先获取表格中原来的信息，如果表格中原来不存在值，就重新赋一个新的值
			self.get_set_ui_from_source()
		else:
			QMessageBox.warning(self, "警告", "已经是最后一个问题！")
	
	def pre_passage_question(self):
		if self.current_index > 0:
			self.current_index -= 1
			self.get_set_ui_from_source()
		else:
			QMessageBox.warning(self, "警告", "已经是第一个问题！")
	
	def init_radio_button(self):
		self.init_radio_answerable()
		self.init_radio_consistent()
	
	#  用来改变按钮的状态，同时改变excel种的值
	def change_answerable(self):
		if self.answerable:
			self.excel_data.loc[self.current_index, 'label'] = "answerable"
		else:
			self.excel_data.loc[self.current_index, 'answer_consistency'] = '0'
		self.init_radio_button()
	
	def change_consistent(self):
		self.excel_data.loc[self.current_index, 'answer_consistency'] = '1' if self.consistent else '0'
		self.init_radio_button()
	
	def set_consistent(self, flag):
		self.consistent = flag
		self.change_consistent()
		print(self.answerable, self.consistent)
		print(self.excel_data.loc[self.current_index, ['label', 'answer_consistency', "备注"]])
	
	def set_answerable(self, flag):
		self.answerable = flag
		if not self.answerable:  # 保证一致性
			self.consistent = False
		self.change_answerable()
		print(self.answerable, self.consistent)
		print(self.excel_data.loc[self.current_index, ['label', 'answer_consistency', "备注"]])
	
	def change_unanswerable_reason(self):
		index = self.comboBox_unanswerable_reason.currentIndex()
		# print(index)
		self.excel_data.loc[self.current_index, 'label'] = "unanswerable:" + self.UNANSWERABLE_REASON_MAP[index]
		print(self.answerable, self.consistent)
		print(self.excel_data.loc[self.current_index, ['label', 'answer_consistency', "备注"]])
		
		# 只有当index == 5 时才会放开
		if index == 5:
			self.lineEdit_unanswerable_notes.setDisabled(False)
	
	def set_notes(self, flag):  # flag =True 说明是other错误
		text = self.lineEdit_unanswerable_notes.text().strip()
		print(text)
		if text == "" and flag:
			QMessageBox.warning(self, "警告", "备注为空")
			return False
		self.excel_data.loc[self.current_index, "备注"] = text
		print(self.excel_data.loc[self.current_index, ['label', 'answer_consistency', "备注"]])
		return True
	
	def get_column_text(self, column_name):
		obj = self.excel_data.loc[self.current_index, column_name]
		if pd.isna(obj):
			return ""
		else:
			return str(obj).strip()
	
	def judge_answerable(self):
		text = self.get_column_text("label")
		if text == "" or text == 'answerable':
			return True
		else:
			return False
	
	def judge_consistent(self):
		text = self.get_column_text("answer_consistency")
		if text == "" or text == '1':
			return True
		else:
			return False
	
	def get_set_ui_from_source(self):
		self.getPassage(self.current_index)
		self.getQuestion(self.current_index)
		self.getAnswer(self.current_index)
		#
		self.answerable = self.judge_answerable()
		# 在这里手动的触发事件
		if self.answerable:
			self.radioButton_answerable.click()
		else:
			self.radioButton_unanswerable.click()
		self.consistent = self.judge_consistent()
		if self.consistent:
			self.radioButton_consistent.click()
		else:
			self.radioButton_unconsistent.click()
		# self.init_radio_button()
		#
		if not self.answerable:
			print("---------")
			print(self.excel_data.loc[self.current_index, ['label', 'answer_consistency', "备注"]])
			print("---------")
			try:
				reason = self.get_column_text("label").split(":")[1]
				index = self.UNANSWERABLE_REASON_MAP2[reason]
			except:
				index = 0
			self.comboBox_unanswerable_reason.setCurrentIndex(index)
		# 
		self.lineEdit_unanswerable_notes.setText(self.get_column_text("备注"))
	
	def init_radio_answerable(self):
		# 初始化组件状态
		if self.answerable:
			self.radioButton_answerable.setChecked(True)
			
			self.radioButton_consistent.setDisabled(False)
			self.radioButton_unconsistent.setDisabled(False)
			
			self.comboBox_unanswerable_reason.setDisabled(True)
			self.lineEdit_unanswerable_notes.setDisabled(True)
		else:
			self.radioButton_unanswerable.setChecked(True)
			self.radioButton_unconsistent.setChecked(True)
			
			self.radioButton_consistent.setDisabled(True)
			self.radioButton_unconsistent.setDisabled(True)
			
			self.comboBox_unanswerable_reason.setDisabled(False)
			self.lineEdit_unanswerable_notes.setDisabled(False)
	
	def init_radio_consistent(self):
		if self.consistent:
			self.radioButton_consistent.setChecked(True)
		else:
			self.radioButton_unconsistent.setChecked(True)
	
	def getAnswer(self, current_index):
		self.textBrowser_answer.setText(self.get_column_text("answer"))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())

'''
label
answerable
unanswerable:specificity
unanswerable:factual consistency
unanswerable:information sufficiency
,,,

answer_consistency
0 1


备注
notes
'''
