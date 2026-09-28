# Ваще это первая версия сделанная на такую скорую руку, ну тут видно)))


from ollama import Client # pip install ollama

from time import time

from colorama import init, Fore, Style # pip install colorama


init()


client = Client(host=f'http://{input("Укажите IP: ").strip()}:{input("Укажите порт: ").strip()}')
models = client.list()


SYSTEM_PROMPT = True


print('\nMichiTheCat-RedStar (c) 2026.\n\n',
	'list - увидеть все модели\n',
	'send - отправить одно сообщение\n',
	'quit - задать IP и PORT\n',
	'connect - диалог с ИИ с сохранением истории\n',
	'pull - не работает')

while True:
	print('\n> list|send|quit|connect|pull')
	
	match input('>>> ').strip().lower():
		case 'list':
			for model in models.models:
				print(model['model'])
		
		case 'send':
			model = input('Введите имя модели: ').strip()
			question = input('Введите запрос: ').strip()
			
			print('\nДумаю...')
			
			history = [{'role': 'user', 'content': question}]
			if SYSTEM_PROMPT:
				history.insert(0, {'role': 'system', 'content': \
				'Do not use any text formatting - the user does not see the formatting.'})
			
			start = time()
			for chunk in client.chat(model=model, messages=history, stream=True):
				if chunk.message.thinking:
					print(Fore.LIGHTBLACK_EX+chunk.message.thinking, end='', flush=True)
				elif chunk.message.content:
					print(Style.RESET_ALL+chunk.message.content, end='', flush=True)
			print('\nОтвечал:', round((time()-start), 2), 'секуд')
		
		case 'quit':
			client = Client(host=f'http://{input("Укажите IP: ").strip()}:{input("Укажите порт: ").strip()}')
			models = client.list()
		
		case 'connect':
			model = input('Введите имя модели: ').strip()
			
			local_history = []
			if SYSTEM_PROMPT: local_history.append({'role': 'system', 'content': \
				'Do not use any text formatting - the user does not see the formatting.'})
			
			print('\nCtrl+C для выхода')
			while True:
				try:
					user = input(Style.RESET_ALL+'\nВведите запрос: ').strip()
				except KeyboardInterrupt:
					break
				try:
					local_history.append({'role': 'user', 'content': user})
					ai_str = ''
					
					print('\nДумаю...')
					start = time()
					for chunk in client.chat(model=model, messages=local_history, stream=True):
						if chunk.message.thinking:
							print(Fore.LIGHTBLACK_EX+chunk.message.thinking, end='', flush=True)
						elif chunk.message.content:
							print(Style.RESET_ALL+chunk.message.content, end='', flush=True)
							ai_str += chunk.message.content
					print('\nОтвечал:', round((time()-start), 2), 'секуд')
					
					local_history.append({'role': 'assistant', 'content': ai_str})
				except KeyboardInterrupt:
					continue
		
		case 'pull':
			try:
				client.pull(input('Имя модели для загрузки: '))
			except Exception as e:
				print(f'Ошибка: {e}\n\nЛучше используйте другую команду!')
