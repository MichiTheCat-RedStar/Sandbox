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

print('Попытка импорта json...', end='', flush=True)
try: from json import dump, load
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта path...', end='', flush=True)
try: from pathlib import Path
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
		print('\nБудет недостуна команда task, ведь модель не поддерживает tool-calling!')
	
	return user


def Generate(question:str, model_name:str, history:list[dict], silent:bool=False) -> str:
	'Генерирует ответ и выводит его'
	
	history.append({'role': 'user', 'content': question})
	result = ''
	
	response = chat(model=model_name, messages=history, think=False, stream=True)
	
	for chunk in response:
		content = chunk.message.content or ''
		if not silent: print(content, end='', flush=True)
		result += content
		
		if chunk.done:
			if not silent: print('\nДумал:', round(chunk.total_duration*0.000000001, 2), 'секунды.')
			break
	
	history.append({'role': 'assistant', 'content': result})
	return result


def AgentLoop(question:str, model_name:str, history:list[dict]) -> str:
	'Генерирует ответ или цепочку вызова инструментов'
	
	... # TODO: реализовать task


def AgentSpaceShow() -> str:
	# Файлы в пространстве агента
	'''Get a list of all files in the space
	
	Returns:
		List of filenames with extensions'''
	
	result = ''
	
	for child in ASSISTANT_PATH.iterdir():
		result += str(child.name)+'\n'
	
	return result.strip()


def AgentSpaceRead(file_name:str) -> str:
	# Читать файл из пространства агента
	'''Reads a file from the space
	
	Args:
		file_name: file name including the extension
	
	Returns:
		file content as text'''
	
	p = Path(ASSISTANT_PATH / file_name)
	if not p.exists():
		return f'The file "{file_name}" does not exist.'
	
	return Path(p).read_text(encoding='utf-8')


def AgentSpaceWrite(file_name:str, content:str) -> str:
	# Записать файл в пространство агента
	'''Write the file to the space
	
	Args:
		file_name: file name including the extension
		content: text content of the file
	
	Returns:
		Creates a file and reports that it has been written or overwritten'''
	
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
			'AgentSpaceShow - показывает файлы в пространстве агента самому агенту',
			'AgentSpaceRead - позволяет агенту читать файлы в своём пространстве',
			'AgentSpaceWrite - позволяет агенту писать в своё пространство'
		]
	}
	
	return tools


# Точка входа
if __name__ == '__main__':
	ASSISTANT_PATH.mkdir(exist_ok=True)
	history, models_list = [], []
	
	print('Загрузки списка моделей...', end='', flush=True)
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
		match input('>>> ').strip().lower():
			case 'quit':
				print('\nУдачи!')
				quit()
			
			case 'send':
				user = input('\nВы > ')
				print('ИИ > ', end='', flush=True)
				Generate(user, model, history)
			
			case 'task':
				if not _HaveTools(model):
					print('\ntask не поддерживается, ведь у модели нет tool-calling!')
				else:
					... # TODO: реализовать task
			
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
	
	# TODO: Сделал минимальный интерфейс для работы, а в дальнейшем
	#        уже надо будет подвязать вызов инструментов, более хорошие
	#        функции с их вызовом и улучшение кода (вроде выбора модели)
	# TODO: Следующим коммитом реализую agentic loop с tool calling
