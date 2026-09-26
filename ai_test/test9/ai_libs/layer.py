# 	ai_test/layer // ☭
# MichiTheCat-RedStar (c) 2026


from .neuron import VectorNeuron #NOTE: Тревожно, так как до этого
                                 #      __init__.py был единсвтенным
                                 #      главным файлом, а теперь дети
                                 #      модуля общаются между собой


class Layer:
	def __init__(self, inputs:int, outputs:int, lr:float=0.01):
		'Уонструктор слоя: линейный векторный вход и векторный выход'
		
		self.Neurons = [VectorNeuron(inputs, lr) for _ in range(outputs)]
		self.LR = lr
	
	
	def Predict(self, questions:list[float]) -> list[float]:
		'Предсказание слоя'
		
		return [n.Predict(questions) for n in self.Neurons]
	
	
	def Train(self, questions:list[float], correct:list[float]) -> list[float]:
		'Обучение слоя'
		
		if len(correct) != len(self.Neurons):
			raise ValueError('Разный размер векторов нейрона и данных!')
		
		return [n.Train(questions, y) for n, y in zip(self.Neurons, correct)]
	
	
	def __str__(self):
		'Узнать актуальные веса и смещения'
		
		return f'Количество нейронов, W и B: {len(self.Neurons)}, {[n.W for n in self.Neurons]} и {[n.B for n in self.Neurons]}'
	
	
	def Educate(self, data:list[tuple], steps:int=1000, output:bool=False):
		'''Итоговое обучение с поколениями
		формат data: (вход:list[float], ответ:list[float])'''
		
		for step in range(1, steps+1):
			for x, y in data:
				self.Train(x, y)
			if output and (step % 100 == 0):
				print(f'Шаг: {step}, {self}')
