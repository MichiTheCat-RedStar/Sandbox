# 	agentic // ☭
# MichiTheCat-RedStar (c) 2026

print('agentic - MichiTheCat-RedStar (c) 2026.')
print('Агент на ollama под локальные модели...\n')
# NOTE: Хардкод пути до файлов так и должны быть, в этом и суть,
#       так же как и в монолитности кода.


# Импорт модулей
print('Попытка импорта ollama...', end='', flush=True)
try: from ollama import chat, show, list as ollama_list, Options
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


print('Инициализация констант...', end='', flush=True)
ASSISTANT_PATH = Path('agent_space')
SYSTEM_PATH = Path('data')
HELP = ('\nВсе доступные команды:'
		'\nhelp  - вывести этот список для справки о командах'
		'\nquit  - выйти из программы'
		'\nsend  - поговорить с ИИ (дать запрос и получить ответ)'
		'\ntask  - дать задачу ИИ (используется AgentLoop с инструментами)'
		'\ntools - посмотреть список инструментов ИИ'
		'\nclear - почистить историю диалога с ИИ'
		'\nmodel - задать модель ИИ'
		'\nsave  - сохранить диалог с ИИ в постоянную память'
		'\nload  - загрузить диалог с ИИ из постоянной памяти'
		'\nconfs - открыть меню настроек переменных окружения (для продвинутых)')
SETTINGS = { # DEFAULTS
	'steps': 6,      # Количество шагов в AgentLoop
	'context': 12,   # Количество сообщений в history
	'livetime': 1,   # Количество минут нахождения модели в памяти
	'threads': 0,    # Сколько используется ядер (0 переводится в None)
	'predict': 4096, # Максимальное количество генерируемых токенов
	'temper': 0.8,   # Температура модели
	'repeat_s': 1.2, # Штраф за повторение токенов
	'repeat_n': 256, # Сколько токенов будет учтено для штрафа
	'sys_prom': '',  # Системный промпт (если нет, то не в history)
	'thinking': 0    # Мышление, которое должно быть 0 или 1
}
print('\b'*3, '[Успешно.]')


# Основной код
def Configurate():
	'Настройки среды'
	
	# Это полноценное отдельное меню, поэтому тут так...
	print('\nДобро пожаловать в настройки окружения среды!')
	ConfLoad()
	
	
	def Show():
		print('\nВот актуальные настройки:')
		for item in SETTINGS:
			print(item, f'[{type(SETTINGS[item]).__name__}] =', SETTINGS[item])
	
	
	def Set():
		print('\nЧто вы хотите поменять?')
		for key in SETTINGS.keys():
			print(key, end=' ', flush=True)
		
		user = input('\n>>> ').strip().lower()
		if user not in SETTINGS.keys():
			print('\nНет такого параметра!')
		else:
			key, item_type = user, type(SETTINGS[user]).__name__
			print('\nКак вы хотите задать парамерт?')
			print('Должно быть:', item_type)
			
			user = input('>>> ').strip()
			try:
				if item_type == 'str':
					SETTINGS[key] = user
				elif item_type == 'float':
					user = float(user)
					if user >= 0:
						SETTINGS[key] = user
					else:
						print('\nЗначение не может быть меньше нуля!')
				elif item_type == 'int':
					user = int(user)
					if user >= 0:
						SETTINGS[key] = user
					else:
						print('\nЗначение не может быть меньше нуля!')
			except (ValueError, TypeError):
				print('\nНе тот тип!')
			else:
				ConfSave()
	
	
	while True:
		print('\nreturn|show|set')
		
		match input('>>> ').strip().lower():
			case 'return': break
			
			case 'show': Show()
			
			case 'set': Set()
			
			case '': pass
			case _: print('\nНеизвестная команда!')


def ConfSave():
	'Сохранение настроек'
	
	SYSTEM_PATH.mkdir(exist_ok=True)
	
	with open(SYSTEM_PATH/'configuration.json', 'w', encoding='utf-8') as f:
		dump(SETTINGS, f, ensure_ascii=False, indent='\t')


def ConfLoad():
	'Загрузка настроек'
	
	global SETTINGS
	
	SYSTEM_PATH.mkdir(exist_ok=True)
	
	try:
		with open(SYSTEM_PATH/'configuration.json', 'r', encoding='utf-8') as f:
			SETTINGS = load(f)
	except FileNotFoundError:
		with open(SYSTEM_PATH/'configuration.json', 'w', encoding='utf-8') as f:
			dump(SETTINGS, f, ensure_ascii=False, indent='\t')


def HistorySave(history:list[dict]):
	'Сохранение истории'
	
	SYSTEM_PATH.mkdir(exist_ok=True)
	
	with open(SYSTEM_PATH/'history.json', 'w', encoding='utf-8') as f:
		dump(history, f, ensure_ascii=False, indent='\t')


def HistoryLoad() -> list[dict]:
	'Загрузка истории'
	
	SYSTEM_PATH.mkdir(exist_ok=True)
	
	try:
		with open(SYSTEM_PATH/'history.json', 'r', encoding='utf-8') as f: return load(f)
	except FileNotFoundError:
		with open(SYSTEM_PATH/'history.json', 'a') as f: pass
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


def _SettingToOptions() -> Options:
	'Превратить настройки в опции Ollama'
	
	return Options(
		num_predict = SETTINGS['predict'],
		temperature = SETTINGS['temper'],
		repeat_penalty = SETTINGS['repeat_s'],
		repeat_last_n = SETTINGS['repeat_n'],
		num_thread = SETTINGS['threads'] or None,
	)


def _SysPrompt(history:list[dict]) -> list[dict]:
	'Вернуть историю вместе с системным промптом'
	
	prompt = SETTINGS.get('sys_prom', '').strip()
	if not prompt:
		return history
	else:
		return [{'role': 'system', 'content': prompt}, *history]


def Generate(question:str, model_name:str, history:list[dict], silent:bool=False) -> str:
	'Генерирует ответ и выводит его'
	
	history.append({'role': 'user', 'content': question})
	result = ''
	
	time_start = time()
	response = chat(model=model_name, messages=_SysPrompt(history), options=_SettingToOptions(), keep_alive=f'{SETTINGS["livetime"]}m', think=bool(SETTINGS['thinking']), stream=True)
	
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


def AgentLoop(question:str, model_name:str, history:list[dict], steps:int) -> str:
	'Генерирует ответ или цепочку вызова инструментов'
	
	tools = ToolsList()['ai']
	tool_map = {func.__name__: func for func in tools}
	history.append({'role': 'user', 'content': question})
	
	time_start = time()
	for _ in range(steps):
		response = chat(model=model_name, messages=_SysPrompt(history), options=_SettingToOptions(), keep_alive=f'{SETTINGS["livetime"]}m', tools=tools, think=bool(SETTINGS['thinking']))
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
	ConfLoad()
	with open(SYSTEM_PATH/'history.json', 'a') as f: pass
	history, models_list = [], []
	print('\b'*3, '[Успешно.]')
	
	print('Загрузка списка моделей...', end='', flush=True)
	for obj in ollama_list().models:
		model = obj.model
		isTools = _HaveTools(model)
		models_list.append({'model': model, 'tools': isTools})
	print('\b'*3, '[Успешно.]')
	
	model = ''
	while not model:
		try:
			model = SetModel(models_list)
		except ValueError:
			print('\nНет такой модели!')
			continue
	
	print(HELP)
	
	while True:
		print('\nhelp|quit|send|task|tools|clear|model|save|load|confs')
		
		try:
			match input('>>> ').strip().lower():
				case 'help':
					print(HELP)
					
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
						AgentLoop(user, model, history, SETTINGS['steps'])
				
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
				
				case 'confs':
					Configurate()
				
				case '': pass
				case _: print('\nНеизвестная команда!')
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
	# TODO: Из SETTINGS осталось реализовать только context
	# TODO: Сделать настройку для того, чтобы автоматически прописывался
	#        SaveHistory() при диалоге с ИИ
