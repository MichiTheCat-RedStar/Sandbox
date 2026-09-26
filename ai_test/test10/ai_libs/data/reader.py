# 	ai_test/data/reader // ☭
# MichiTheCat-RedStar (c) 2026


from pathlib import Path
from json import loads


def ReadData(file_path:str, no_dataset:bool=False) -> list[tuple]:
	'Ядро для чтния файлов'
	
	# Проверка валидности и объявление пути
	if no_dataset:
		p = Path(file_path)
	else:
		p = Path('dataset/'+file_path)
	if (not p.is_file()) and (not p.exists()):
		raise ValueError('Указан не файл!')
	
	# Чтение файла
	result = []
	with open(p, 'r', encoding='utf-8') as f:
		
		meta_data = loads(f.readline())
		
		for line in f:
			line = line.strip()
			if (not line) or (line[0] == '#'): continue
			
			line_data = loads(line)
			
			'''
			# Валидатор
			if (meta_data['in'] == 'txt') and  (line_data['in'] is str):
				... # как же много писать
			'''
			
			# FIXME: временный костыль
			result.append((line_data['in'], line_data['out']))
	
	return result
