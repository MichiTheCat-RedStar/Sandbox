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
	data = ReadTeachData('synthetic_train_emotion.txt')
	pprint(data)
