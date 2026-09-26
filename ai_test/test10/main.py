# 	ai_test // ☭
# MichiTheCat-RedStar (c) 2026

print('ai_test - MichiTheCat-RedStar (c) 2026.')
print('Тестирую нейросети и работу с ними...\n')


# Импорт модулей
print('Попытка импорта ai_libs...', end='', flush=True)
try: from ai_libs import *
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')


# Точка входа
if __name__ == '__main__':
	print('\nСоздание слоя и выведение весов:')
	
	n = Layer(2, 2)
	
	n.Educate([
		([0, 0], [0, 0]),
		([2, 3], [5, -1]),
		([5, 2], [7, 3]),
		([-2, 1], [-1, -3]),
		([-1, -3], [-4, 2]),
	], 100) # 100 вполне достаточно, даже 50 поколений
	
	for ni, neu in enumerate(n.Neurons):
		for wi, w in enumerate(neu.W):
			print(f'Нейрон {ni}, вес {wi}: {w:.2f}')
	
	
	print('\nНа основе этих весов предугадываю:')
	for a in range(1, 12):
		for b in range(1, 12):
			answer = n.Predict([a, b])
			print(f'{a}+{b} = {answer[0]:.1f}; {a}-{b} = {answer[1]:.1f}', end=' | ')
	
	# Выше был тест потыкать все эти имена.атрибуты и прочее, теперь
	# я на основе этого смогу сделать нормальный модуль saves.py
	
