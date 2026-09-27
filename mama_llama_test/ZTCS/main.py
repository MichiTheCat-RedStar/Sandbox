# Ваще это первая версия сделанная на такую скорую руку, ну тут видно)))


from ollama import Client # pip install ollama

from time import time


client = Client(host=f'http://{input("Укажите IP: ").strip()}:{input("Укажите порт: ").strip()}')
models = client.list()


SYSTEM_PROMPT = True


while True:
	print('\n> list|send')
	
	match input('>>> ').strip().lower():
		case 'list':
			for model in models.models:
				print(model['model'])
		
		case 'send':
			model = input('Введите имя модели: ').strip()
			question = input('Введите запрос: ').strip()
			
			print('\nДумаю...', end='', flush=True)
			start = time()
			
			history = [{'role': 'user', 'content': question}]
			if SYSTEM_PROMPT:
				history.insert(0, {'role': 'system', 'content': \
				'Do not use any text formatting - the user does not see the formatting.'})
			
			response = client.chat(model=model, messages=history)
			
			print('\r'+response.message.content)
			print('Думал:', round((time()-start), 2), 'секуд')
