# 	agentic // ☭
# MichiTheCat-RedStar (c) 2026

print('agentic - MichiTheCat-RedStar (c) 2026.')
print('Агент на ollama под маленькие модели...\n')
# NOTE: Хардкод пути до файлов так и должны быть, в этом и суть,
#       так же как и в монолитности кода.


# Импорт модулей
print('Попытка импорта ollama...', end='', flush=True)
try: from ollama import chat, show, list as ollama_list
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта time...', end='', flush=True)
try: from time import time
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта json...', end='', flush=True)
try: from json import dump, load
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')


# Основной код
def HistorySave(history:list[dict]):
	'Сохранение истории'
	
	with open('history', 'w', encoding='utf-8') as f:
		dump(history, f, ensure_ascii=False, indent='\t')


def HistoryLoad() -> list[dict]:
	'Загрузка истории'
	
	try:
		with open('history', 'r', encoding='utf-8') as f: return load(f)
	except FileNotFoundError:
		return []


def _HaveTools(model_name:str) -> bool:
	'Есть ли ToolCalling у модели'
	
	return 'tools' in show(model_name).capabilities


def Generate(question:str, model_name:str, history:list[dict]=[], silent:bool=False) -> str:
	'Генерирует ответ и выводит его'
	
	history.append({'role': 'user', 'content': question})
	result = ''
	
	response = chat(model=model_name, messages=history, think=False, stream=True)
	
	for chunk in response:
		content = chunk.message.content
		if not silent: print(content, end='', flush=True)
		result += content
	
	if chunk.get('done'):
		if not silent: print('\nДумал:', round(chunk.total_duration*0.000000001, 2), 'секунд.')
		history.append({'role': 'assistant', 'content': result})
	
	return result


# Точка входа
if __name__ == '__main__':
	history = []
	
	models = [] # TODO: если не подходит, то включать режим "Только текст"
	print('\nВот список ваших моделей:')
	for obj in ollama_list().models:
		model = obj.model
		models.append(model)
		print('[Подходит]   ' if _HaveTools(model) else '[Не подходит]', model)
	model = input('\nВведите имя модели: ').strip()
	if not (model in models):
		raise ValueError('Нет такой модели!')
	
	while True:
		print('\nquit|send|clear|model|save|load')
		match input('>>> ').strip().lower():
			case 'quit':
				print('\nУдачи!')
				quit()
			
			case 'send':
				user = input('\nВы > ')
				print('ИИ > ', end='', flush=True)
				Generate(user, model, history)
			
			case 'clear':
				history = []
				print('\nИстория диалога очищена!')
			
			case 'model':
				print('\nВыберите модель:')
				for m in models:
					print(m)
				user = input('\nВведите имя модели: ').strip()
				if not (model in models):
					print('\nТакой модели нет, используется прошлая!')
				else:
					model - user
			
			case 'save':
				HistorySave(history)
				print('\nИстория сохранена!')
			
			case 'load':
				history = HistoryLoad()
				print('\nИстория загружена!')
	
	# TODO: Сделал минимальный интерфейс для работы, а в дальнейшем
	#       уже надо будет подвязать вызов инструментов, более хорошие
	#       функции с их вызовом и улучшение кода (вроде выбора модели)
