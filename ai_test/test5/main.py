# 	ai_test // ☭
# MichiTheCat-RedStar (c) 2026

from string import printable
from pprint import pprint

from ai_libs import neuron


def ReadData(file_name:str) -> list:
	'Чтение файла и превращение в список из запроса и ответа'
	
	result = []
	with open(file_name, 'r', encoding='utf-8') as f: content = f.read()
	content = content.strip()
	data_lines = content.split('\n')
	for line in data_lines:
		line = line.strip()
		if ' <ai> ' not in line: continue
		user, ai = line.split(' <ai> ', 1)
		user = user.removeprefix('<usr> ')
		result.append((user, ai))
	
	return result


def BuildVocab(text:str):
	'Строит словарь символ в id и обратно'
	
	chars = sorted(set(text))
	stoi = {c: i for i, c in enumerate(chars)}
	itos = {i: c for c, i in stoi.items()}
	return stoi, itos


# TEST
if __name__ == '__main__':
	...
