# 	agentic // ☭
# MichiTheCat-RedStar (c) 2026

print('agentic - MichiTheCat-RedStar (c) 2026.')
print('Агент на ollama под маленькие модели...\n')
# NOTE: Хардкод пути до файлов так и должны быть, в этом и суть,
#       так же как и в монолитности кода.
# TODO: Сменить сохранение на JSON, но пока работает из-за отсутствия
#       многострочного ввода.


# Импорт модулей
print('Попытка импорта ollama...', end='', flush=True)
try: from ollama import chat, show
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта time...', end='', flush=True)
try: from time import time
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')


# Основной код
def HistorySave(history:list[dict]):
	'Сохранение истории'
	
	data = ''
	
	for message in history:
		data += message['role']+'\n'+message['content']+'\n'
	
	with open('history', 'w', encoding='utf-8') as f: f.write(data)


def HistoryLoad() -> list[dict]:
	'Загрузка истории'
	
	try:
		with open('history', 'r', encoding='utf-8') as f: data = f.read()
	except FileNotFoundError:
		print('Сохранение не найдено!')
	else:
		
		history = data.strip().split('\n')
		if history[0] == '': return []
		
		result = []
		for line in range(0, len(history), 2):
			role = history[line]
			content = history[line+1]
			
			result.append({'role':role, 'content':content})
		
		return result


def _HaveTools(model_name:str) -> bool:
	'Есть ли ToolCalling у модели'
	
	return 'tools' in show(model_name).capabilities


# Точка входа
if __name__ == '__main__':
	history = []
	
	print(_HaveTools('qwen2.5:0.5b'))
	
	# TODO: продолжить писать функции
