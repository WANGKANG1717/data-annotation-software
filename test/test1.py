# -*- coding: utf-8 -*-
# @Datetime : 2023/9/30 10:10
# @Author   : WANGKANG
# @Blog     : kang17.xyz
# @File     : test1.py
# @brief    : 测试excel文件的读写
# Copyright 2023 WANGKANG, All Rights Reserved.
import pandas as pd
from pandas import DataFrame
import random
import hashlib
import requests


def translate_en2zh(text):
	def md5(data):
		# appid + q + salt + 密钥
		str = data["appid"] + data["q"] + data["salt"] + KEY
		return hashlib.md5(str.encode("utf-8")).hexdigest()
	
	def random_num_10():
		return str(random.randint(10 ** 9, 10 ** 10 - 1))
	
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43'
	}
	
	url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
	
	KEY = 'XZwpfN_VJ13VSXLhSYp5'
	APPID = "20230930001833627"
	
	data = {
		'q': text.strip().replace("\n", "@@"),
		'from': "en",
		'to': "zh",
		'appid': APPID,
		'salt': random_num_10(),
		'sign': "",
	}
	data["sign"] = md5(data)
	# print(data)
	json_data = requests.post(url=url, headers=headers, data=data).json()
	# print(json_data)
	if json_data.get('trans_result') is not None:
		res = json_data['trans_result'][0]['dst']
		res = res.replace("@@", "\n")
		return res
	else:
		return json_data['error_msg']


if __name__ == '__main__':
	text = '''
A pine is any conifer in the genus Pinus, , of the family Pinaceae.  "Pinus" is the sole genus in the subfamily Pinoideae.  The Plant List compiled by the Royal Botanic Gardens, Kew and Missouri Botanical Garden accepts 126 species names of pines as current, together with 35 unresolved species and many more synonyms.
Butea is a genus of flowering plants belonging to the pea family, Fabaceae.  It is sometimes considered to have only two species, "B. monosperma" and "B. superba", or is expanded to include four or five species.
	'''
	res = translate_en2zh(text)
	print(res)
# excel_data = pd.read_excel('./flant5-base-hotpot-fewshot.xlsx')
# excel_data.loc[0, 'answer_consistency'] = 1
# print(excel_data.loc[0])
# print(excel_data.loc[0, 'passage'])
# print(len(excel_data['passage']))
# print(type(excel_data.loc[0, 'answer_consistency']))
# print(str(excel_data.loc[90, 'label']))
# print(pd.isna(excel_data.loc[90, 'label']))
# print(excel_data.loc[0, ['label', 'answer_consistency', "备注"]])
# print(pd.isna(excel_data.loc[0, 'label']) or excel_data.loc[0, 'label'].strip() == "")
# print(excel_data.columns)
'''
file_path = r'./new.xlsx'
df = pd.read_excel(file_path)
print(df)
print(df.columns)
# print(df['name'])
# print(df['age'])
# print(df['gender'])

# 使用这种方式会报警告，所以应避免使用这种方式
# df['name'][0] = '测试修改数据'
df.loc[0, 'name'] = '测试修改数据'
print(df.name[0])
'''

# print(type(df['age'][1]))
# df['age'][1] = 21
# print(df)
#
# DataFrame(df).to_excel("./new2.xlsx", sheet_name='Sheet1', index=False, header=True)

# 写Excel
# data = { 'name': ['zs', 'ls', 'ww'], 'age': [11, 12, 13], 'gender': ['man', 'man', 'woman']}
# df = pd.DataFrame(data)
# df.to_excel('new.xlsx')


# 读Excel
# file_path = r'./flant5-base-hotpot-fewshot.xlsx'
# df = pd.read_excel(file_path, sheet_name = "Sheet1")
# # 打印表数据，如果数据太多，会略去中间部分
# print(df)
#
# print("=" * 50)
# # 打印头部数据，仅查看数据示例时常用
# print(df.head())
# print("=" * 50)
# # 打印列标题
# print(df.columns)
# print("=" * 50)
# # 打印行
# print(df.index)
# print("=" * 50)
# # 打印指定列
# print(df["passage"])
# print("=" * 50)
# # 描述数据
# print(df.describe())
