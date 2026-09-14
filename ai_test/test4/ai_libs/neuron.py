# 	ai_test/neuron // ☭
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
	
	
	def Educate(self, data:tuple, steps:int=1000, output:bool=False):
		'''Итоговое обучение с поколениями
		формат data: (правильный_ответ, чему_учат)'''
		
		for step in range(1, steps+1):
			for x, y in data:
				self.Train(x, y)
			if (step % 1000 == 0) and output:
				print(f'Шаг: {step}, {self}')
