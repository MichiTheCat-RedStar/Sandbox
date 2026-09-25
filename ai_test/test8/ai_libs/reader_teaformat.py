# 	ai_test/reader_teaformat // ☭
# MichiTheCat-RedStar (c) 2026

from pathlib import Path


def _ReadCore(file_path:str, template:tuple, no_dataset:bool=False) -> list:
	'Ядро для чтния файлов'
	
	# Проверка валидности и объявление пути
	if no_dataset:
		p = Path(file_path)
	else:
		p = Path('dataset/'+file_path)
	if (not p.is_file()) and (not p.exists()):
		raise ValueError('Указан не файл!')
	
	# Шаблонизатор
	t_first, t_second = template # Пример: (<usr>, <ai>)
	
	# Создание списка
	result = []
	
	with open(p, 'r', encoding='utf-8') as f: content = f.read()
	content = content.strip()
	data_lines = content.split('\n')
	
	for line in data_lines:
		line = line.strip()
		
		# Фильтр от лишнего
		if (not line) or (line[0] == '#') or \
		  (f' {t_second} ' not in line) or \
		  (f'{t_first} ' not in line): continue
		
		first, second = line.split(f' {t_second} ', 1)
		first = first.removeprefix(f'{t_first} ')
		result.append((first, second))
	
	return result


def ReadTextData(file_name:str) -> list:
	'''Возвращает список кортежей вида:
	(данные_для_обучения:str, ответ:str)'''
	
	data = _ReadCore(file_name, ('<usr>', '<ai>'))
	
	result = []
	for obj in data:
		result.append((obj[0], obj[1]))
	
	return result


def ReadTeachData(file_name:str) -> list:
	'''Возвращает список кортежей вида:
	(данные_для_обучения:str, ответ:float)'''
	
	data = _ReadCore(file_name, ('<data>', '<fact>'))
	
	result = []
	for obj in data:
		result.append((obj[0], float(obj[1])))
	
	return result


def ReadIntData(file_name:str) -> list:
	'''Возвращает список кортежей вида:
	(данные_для_обучения:float, ответ:float)'''
	
	data = _ReadCore(file_name, ('<in>', '<out>'))
	
	result = []
	for obj in data:
		result.append((float(obj[0]), float(obj[1])))
	
	return result


def BuildVocab(text:str) -> tuple:
	'Строит кортеж символ в id и обратно'
	
	chars = sorted(set(text))
	stoi = {c: i for i, c in enumerate(chars)}
	itos = {i: c for c, i in stoi.items()}
	return (stoi, itos)


# TODO: Мне нравится то, что у меня свой формат данных, однако это явно
#       не верный формат из-за того, как реализован парсинг...
#       В будущем явно надо будет перейти на читаемый JSONL - парсить
#       его, но если json-модуль это не умеет, то брать каждую строку по
#       отдельности и прогонять через json-модель
