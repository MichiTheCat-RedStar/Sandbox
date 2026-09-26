# 	ai_test // ☭
# MichiTheCat-RedStar (c) 2026

print('ai_test - MichiTheCat-RedStar (c) 2026.')
print('Тестирую нейросети и работу с ними...\n')


# Импорт модулей
print('Попытка импорта pprint...', end='', flush=True)
try: from pprint import pprint
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта ai_libs...', end='', flush=True)
try: from ai_libs import *
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')


# Точка входа
if __name__ == '__main__':
	print('\nМатериал обучения:')
	data = ReadData('num-bool_alg_IsEven.jsonl')
	pprint(data)
	
	print('\nСоздание векторного нейрона:')
	n = Neuron()
	print('Нейрон создан:', n)
	
	print('\nОбучения на данных:')
	n.Educate(data)
	print('Обучен!')
	
	# Опять я забыл, что это линейная функция и она не счиатет как 0, 1, 0, 1...
	print('\nТеперь он должен определять, чётное число или нет:')
	while True:
		try: user = float(input('Ты> '))
		except: continue
		
		print('Чётно' if (n.Predict(user) >= 0.5) else 'Нечётно')
