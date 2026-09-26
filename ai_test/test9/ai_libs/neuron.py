# 	ai_test/neuron // ☭
# MichiTheCat-RedStar (c) 2026


class Neuron:
	def __init__(self, w:float=0.0, b:float=0.0, lr:float=0.01):
		'Конструктор нейрона: Линейный один вход и один выход'
		
		self.W  = w  # weight        | вес входа
		self.B  = b  # bias          | смещение
		self.LR = lr # learning rate | скорость обучения
	
	
	def Predict(self, question:float) -> float:
		'Предсказывание'
		
		return self.W * question + self.B
	
	
	def Train(self, question:float, correct:float) -> float:
		'Обучение'
		
		error = correct - self.Predict(question)
		self.W += self.LR * error * question
		self.B += self.LR * error
		return error
	
	
	def __str__(self):
		'Узнать актуальный вес и смещение'
		
		return f'W и B: {self.W:.2f} и {self.B}'
	
	
	def Educate(self, data:list[tuple], steps:int=1000, output:bool=False):
		'''Итоговое обучение с поколениями
		формат data: (вход:float, ответ:float)'''
		
		for step in range(1, steps+1):
			for x, y in data:
				self.Train(x, y)
			if (step % 1000 == 0) and output:
				print(f'Шаг: {step}, {self}')



class VectorNeuron:
	def __init__(self, size:int, lr:float=0.01):
		'Конструктор векторного нейрона: Линейный векторный вход и один выход'
		
		self.W  = [0.0] * size # weight        | вес входа
		self.B  = 0.0          # bias          | смещение
		self.LR = lr           # learning rate | скорость обучения
	
	
	def Predict(self, questions:list[float]) -> float:
		'Предсказывание'
		
		if len(questions) != len(self.W):
			raise ValueError('Разный размер векторов нейрона и данных!')
		
		return sum(w * qi for w, qi in zip(self.W, questions)) + self.B
	
	
	def Train(self, questions:list[float], correct:float) -> float:
		'Обучение'
		
		error = correct - self.Predict(questions)
		
		for i in range(len(self.W)):
			self.W[i] += self.LR * error * questions[i]
		
		self.B += self.LR * error
		return error
	
	
	def __str__(self):
		'Узнать актуальный вес и смещение'
		
		return f'W и B: {self.W} и {self.B}'
	
	
	def Educate(self, data:list[tuple], steps:int=1000, output:bool=False):
		'''Итоговое обучение с поколениями
		формат data: (вход:list[float], ответ:float)'''
		
		for step in range(1, steps+1):
			for x, y in data:
				self.Train(x, y)
			if (step % 100 == 0) and output:
				print(f'Шаг: {step}, {self}')
