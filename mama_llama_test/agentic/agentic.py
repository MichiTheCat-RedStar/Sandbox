# 	agentic // ☭
# MichiTheCat-RedStar (c) 2026

print('agentic - MichiTheCat-RedStar (c) 2026.')
print('Агент на ollama под локальные модели...\n')
# NOTE: Хардкод пути до файлов так и должны быть, в этом и суть,
#       так же как и в монолитности кода.


# Импорт модулей
print('Попытка импорта ollama...', end='', flush=True)
try: from ollama import chat, show, list as ollama_list
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта json...', end='', flush=True)
try: from json import dump, load
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта path...', end='', flush=True)
try: from pathlib import Path
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта time...', end='', flush=True)
try: from time import time
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')


ASSISTANT_PATH = Path('agent_space')


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


def SetModel(models:list[dict]) -> str:
	'Задать модель'
	
	models_list = []
	print('\nВот список ваших моделей:')
	for model in models:
		models_list.append(model['model'])
		print('[Подходит]   ' if model['tools'] else '[Не подходит]', model['model'])
	
	user = input('\nВведите имя модели: ').strip()
	if not (user in models_list):
		raise ValueError('Нет такой модели!')
	
	if not _HaveTools(user):
		print('\nБудет недоступна команда task, ведь модель не поддерживает tool-calling!')
	
	return user


def Generate(question:str, model_name:str, history:list[dict], silent:bool=False) -> str:
	'Генерирует ответ и выводит его'
	
	history.append({'role': 'user', 'content': question})
	result = ''
	
	time_start = time()
	response = chat(model=model_name, messages=history, think=False, stream=True)
	
	for chunk in response:
		content = chunk.message.content or ''
		if not silent: print(content, end='', flush=True)
		result += content
		
		if chunk.done:
			if not silent: print('\n\nЗаняла генерация:', round(chunk.eval_duration*0.000000001, 2), 'секунды.')
			break
	
	if not silent: print('Заняло времени:', round(time()-time_start, 2), 'секунды.')
	history.append({'role': 'assistant', 'content': result})
	return result


def AgentLoop(question:str, model_name:str, history:list[dict], steps:int=6) -> str:
	'Генерирует ответ или цепочку вызова инструментов'
	
	tools = ToolsList()['ai']
	tool_map = {func.__name__: func for func in tools}
	history.append({'role': 'user', 'content': question})
	
	time_start = time()
	for _ in range(steps):
		response = chat(model=model_name, messages=history, tools=tools, think=False)
		message = response.message
		history.append(message.model_dump(exclude_none=True))
		
		if not message.tool_calls:
			answer = message.content or ''
			print('\nИИ >', answer)
			print('\nЗаняло времени:', round(time()-time_start, 2), 'секунды.')
			return answer
		
		for call in message.tool_calls:
			name = call.function.name
			args = call.function.arguments or {}
			print(f'[Инструмент] {name}')
			
			func = tool_map.get(name)
			try:
				result = func(**args) if func else f'Unknown tool: {name}'
			except Exception as error:
				result = f'Error in `{name}`: {error}'
			
			print(f'[Ответ] {result}\n')
			history.append({'role': 'tool', 'tool_name': name, 'content': str(result)})
	
	print('[Лимит шагов исчерпан.]')
	print('\nЗаняло времени:', round(time()-time_start, 2), 'секунды.')
	return ''


def AgentSpaceShow() -> str:
	# Файлы в пространстве агента
	'''Get a list of all files in the space
	
	Returns:
		List of filenames with extensions'''
	
	result = ''
	ASSISTANT_PATH.mkdir(exist_ok=True)
	
	for child in ASSISTANT_PATH.iterdir():
		result += str(child.name)+'\n'
	
	result = result.strip()
	
	if result:
		return result
	else:
		return 'No files in the directory.'


def AgentSpaceRead(file_name:str) -> str:
	# Читать файл из пространства агента
	'''Reads a file from the space
	
	Args:
		file_name: file name including the extension
	
	Returns:
		file content as text'''
	
	ASSISTANT_PATH.mkdir(exist_ok=True)
	
	p = Path(ASSISTANT_PATH / file_name)
	if not p.exists():
		return f'The file "{file_name}" does not exist.'
	
	return p.read_text(encoding='utf-8')


def AgentSpaceWrite(file_name:str, content:str) -> str:
	# Записать файл в пространство агента
	'''Write the file to the space
	
	Args:
		file_name: file name including the extension
		content: text content of the file
	
	Returns:
		Creates a file and reports that it has been written or overwritten'''
	
	ASSISTANT_PATH.mkdir(exist_ok=True)
	
	isRewrite = False
	p = Path(ASSISTANT_PATH / file_name)
	
	if p.exists(): isRewrite = True
	p.write_text(content, encoding='utf-8')
	
	if isRewrite:
		return f'"{file_name}" was overwritten.'
	else:
		return f'The text is recorded in "{file_name}"'


def ToolsList() -> dict:
	'Вернуть список инструментов для ИИ или пользователя'
	
	tools = {
		'ai': [AgentSpaceShow, AgentSpaceRead, AgentSpaceWrite],
		'user': [
			'AgentSpaceShow  - показывает файлы в пространстве агента самому агенту',
			'AgentSpaceRead  - позволяет агенту читать файлы в своём пространстве',
			'AgentSpaceWrite - позволяет агенту писать в своё пространство'
		]
	}
	
	return tools


# Точка входа
if __name__ == '__main__':
	print('Инициализация настроек и файлов...', end='', flush=True)
	ASSISTANT_PATH.mkdir(exist_ok=True)
	with open('history', 'a') as f: pass
	history, models_list = [], []
	print('\b'*3, '[Успешно.]')
	
	print('Загрузка списка моделей...', end='', flush=True)
	for obj in ollama_list().models:
		model = obj.model
		isTools = _HaveTools(model)
		models_list.append({'model': model, 'tools': isTools})
	print('\b'*3, '[Успешно.]')
	model = SetModel(models_list)
	
	print('\nВсе доступные команды:'
		'\nquit  - выйти из программы'
		'\nsend  - поговорить с ИИ (дать запрос и получить ответ)'
		'\ntask  - дать задачу ИИ (используется AgentLoop с инструментами)'
		'\ntools - посмотреть список инструментов ИИ'
		'\nclear - почистить историю диалога с ИИ'
		'\nmodel - задать модель ИИ'
		'\nsave  - сохранить диалог с ИИ в постоянную память'
		'\nload  - загрузить диалог с ИИ из постоянной памяти')
	
	while True:
		print('\nquit|send|task|tools|clear|model|save|load')
		
		try:
			match input('>>> ').strip().lower():
				case 'quit':
					print('\nУдачи!')
					break
				
				case 'send':
					user = input('\nВы > ')
					print('ИИ > ', end='', flush=True)
					Generate(user, model, history)
				
				case 'task':
					if not _HaveTools(model):
						print('\ntask не поддерживается, ведь у модели нет tool-calling!')
					else:
						user = input('\nВы > ')
						print('ИИ работает...')
						AgentLoop(user, model, history)
				
				case 'tools':
					print('\nВот список инструментов у агента:')
					for tool in ToolsList()['user']:
						print(tool)
				
				case 'clear':
					history = []
					print('\nИстория диалога очищена!')
				
				case 'model':
					try:
						model = SetModel(models_list)
					except ValueError:
						print('\nНет такой модели: оставлена предыдущая.')
				
				case 'save':
					HistorySave(history)
					print('\nИстория сохранена!')
				
				case 'load':
					history = HistoryLoad()
					print('\nИстория загружена!')
		except KeyboardInterrupt: print(); continue
	
	# TODO: Сделал минимальный интерфейс для работы, а в дальнейшем
	#        уже надо будет подвязать вызов инструментов, более хорошие
	#        функции с их вызовом и улучшение кода (вроде выбора модели)
	# TODO: Всё готово и осталось только добавлять больше инструментов!)
	# TODO: Сжимать историю, удалять последние сообщения или типа того,
	#        а так же можно сделать настройки для системного промпта и
	#        для количества лимита шагов для агента
	# TODO: Так же раз не так хорошо получилось с маленькими моделями,
	#        то можно взять вектор под более крупные модели
	# TODO: Сделать защиту путей и прочей безопасности
	# TODO: Создать функцию для автоматического создания agent_space/ и
	#        валидации пути, чтобы обрезать возможным обращаться к /..
