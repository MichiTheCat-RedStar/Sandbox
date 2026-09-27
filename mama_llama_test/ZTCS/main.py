# Ваще это первая версия сделанная на такую скорую руку, ну тут видно)))


from ollama import Client # pip install ollama

from time import time

client = Client(host=f'http://{input("Укажите IP: ").strip()}:{input("Укажите порт: ").strip()}')
models = client.list()


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
			
			response = client.chat(model=model, messages=[{'role': 'user', 'content': question}])
			
			print('\r'+response.message.content)
			print('Думал:', round((time()-start), 2), 'секуд')
