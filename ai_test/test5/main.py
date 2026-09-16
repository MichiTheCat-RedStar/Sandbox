# 	ai_test // ☭
# MichiTheCat-RedStar (c) 2026

from string import printable
from pprint import pprint

from ai_libs import Neuron


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
	data = ReadData('dataset/synthetic_data_universal_1_creative.txt')
	pprint(data)
	print()
	char_data = BuildVocab(printable)
	pprint(char_data)
	
	n = Neuron(lr=0.001)
	
	dataset = []
	for block in data:
		user, ai = [], []
		for c in block[0]:
			user.append(str(char_data[0].get(c, c)))
		for c in block[1]:
			ai.append(str(char_data[0].get(c, c)))
		dataset.append((int(''.join(user)), int(''.join(ai))))
	
	pprint(dataset)
	
	
	#n.Educate(dataset, 100000, True)
	n.Educate(dataset, 100, True)
	
	print('Обучено:')
	while True:
		user = input('\nТы: ')
		
		# Перевожу как с dataset значения в числа
		user_int = []
		for c in user:
			user_int.append(str(char_data[0].get(c, c)))
		user = int(''.join(user_int))
		
		ai = str(n.Predict(user))
		
		ai_buffer = []
		for c in ai: # ????????
			ai_buffer.append(str(char_data[0].get(c, c)))
		ai = ''.join(ai_buffer)
		
		print('ИИ: ', end='', flush=True)
		for num in ai:
			print(char_data[0][num], end='', flush=True)
