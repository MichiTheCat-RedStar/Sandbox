# 	ai_test/reader_teaformat // ☭
# MichiTheCat-RedStar (c) 2026


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


def BuildVocab(text:str) -> tuple:
	'Строит кортеж символ в id и обратно'
	
	chars = sorted(set(text))
	stoi = {c: i for i, c in enumerate(chars)}
	itos = {i: c for c, i in stoi.items()}
	return (stoi, itos)


'''
def BuildTokens(text:list) -> tuple: #NOTE: Токенизирует целые слова!!!
	'Строит кортеж слова в id и обратно'
	
	for word in list:
		...
'''


def ReadTeachData(file_name:str) -> list:
	'''Возвращает список кортежей кортеж вида:
	(данные_для_обучения:float, ответ:float)'''
	
	result = []
	with open(file_name, 'r', encoding='utf-8') as f: content = f.read()
	content = content.strip()
	data_lines = content.split('\n')
	for line in data_lines:
		line = line.strip()
		if not line: continue
		if line[0] == '#': continue
		if ' <fact> ' not in line: continue
		user, ai = line.split(' <fact> ', 1)
		user = user.removeprefix('<data> ')
		result.append((user, float(ai)))
	
	return result


# TODO: Мне нравится то, что у меня свой формат данных, однако это явно
#       не верный формат из-за того, как реализован парсинг...
#       В будущем явно надо будет перейти на читаемый JSONL - парсить
#       его, но если json-модуль это не умеет, то брать каждую строку по
#       отдельности и прогонять через json-модель
