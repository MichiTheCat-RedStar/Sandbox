# 	ai_test // ☭
# MichiTheCat-RedStar (c) 2026

from pprint import pprint

LR = 1
W = 1


def MathFormular() -> dict:
	'Возвращает формулу и правильный ответ'
	
	result = {}
	
	for a in range(10):
		for b in range(10):
			for symb in list('+-'):
				formula = f'{a}{symb}{b}'			# Формируем формулу
				if eval(formula) < 0: continue		# Пропускаем отрицательные числа
				result[formula] = f'{eval(formula)}'# Сохраняем результат
	
	return result


def DictToList(formulas:dict) -> list:	#NOTE: Я мог делать сразу в виде словаря, но тупанул и это костыль, исправлю в будущем
	'Превращаем Словарь в Список'
	
	result = []
	
	for key, value in formulas.items():
		result.append((key, value))
	
	return result


def Teaching(data:tuple):
	'Обучение ИИ на кортеже'
	
	global W
	STEPS = 100
	
	for step in range(STEPS):
		for x, correct in data:
			guess = W * x
			error = int(correct) - guess
			W = W + LR * error * x
		print(f"шаг {step:2d}  w = {w:.4f}")
	
	#FIXME: Я не буду дописывать и чинить код, я понял что занимаюсь не
	#       тем, мне надо сделать так, чтобы код счиатл числа, но я бы
	#       использовал всего один нейрон, поэтому я долежн выдавать
	#       булево значение, либо второй нейрон добавить для 2D вектора,
	#       от чего бы я смог уже выбирать число через ИИ...
	#       Как раз в следующей версии я костыль уберу и за одно сделаю
	#       нормальный код, а не это...


# TEST
if __name__ == '__main__':
	forms = MathFormular()
	pprint(forms)
	forms = DictToList(forms)
	pprint(forms)
	Teaching(forms)
