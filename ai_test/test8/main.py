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
	'''
	print('\nМатериал обучения:')
	data = ReadTeachData('synthetic_train_emotion.txt')
	pprint(data)
	'''
	
	print('\nСоздание векторного нейрона:')
	n = VectorNeuron(5, 0.1)
	print('Нейрон создан:', n)
	
	print('\nОбучение нейрона:')
	n.Educate([([0, 0, 0, 0, 0], 0), ([1, 1, 1, 1, 1], 1)], 1000, True)
	# Фактически не имеет смысла, просто пытался сделать что-то дял вида
	
	print('\nПредугадывание:')
	print('Должно быть 0.0:', round(n.Predict([0, 0, 0, 0, 0]), 1))
	print('Должно быть 1.0:', round(n.Predict([1, 1, 1, 1, 1]), 1))
	print('В идеале должно быть 0.5:', round(n.Predict([0.5, 0.5, 0.5, 0.5, 0.5]), 2))
	print('В идеале должно быть 0.4:', round(n.Predict([0, 1, 0, 1, 0]), 2))
	print('В идеале должно быть 2.0:', round(n.Predict([2, 2, 2, 2, 2]), 1))
	print('В идеале должно быть -1.2:', round(n.Predict([-1.2, -1.2, -1.2, -1.2, -1.2]), 2))
