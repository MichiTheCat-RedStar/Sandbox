# 	ai_test // ☭
# MichiTheCat-RedStar (c) 2026


class Neuron:
	def __init__(self, w:float=0.0, b:float=0.0, lr:float=0.01):
		'Конструктор нейрона'
		
		self.W  = w  # weight        | вес входа
		self.B  = b  # bias          | смещение
		self.LR = lr # learning rate | скорость обучения
	
	
	def Predict(self, question:float) -> float:
		'Предсказывание'
		
		return self.W * question + self.B
	
	
	def Train(self, question:float, correct:float):
		'Обучение'
		
		error = correct - self.Predict(question)
		self.W += self.LR * error * question
		self.B += self.LR * error
	
	
	def __str__(self):
		'Узнать актуальный вес и смещение'
		
		return f'W и B: {self.W:.2f} и {self.B}'


# TEST
if __name__ == '__main__':
	n = Neuron()
	
	for step in range(1, 10001):
		for x in range(10):
			n.Train(x, x*2)
		if step % 1000 == 0:
			print(f'Шаг: {step}, {n}')
	
	print('\nНапишите число, нейрон должен умножить его на два:')
	while True:
		try:
			user = float(input('> '))
		except ValueError:
			print('Неправильный ввод')
		else:
			print(n.Predict(user))
