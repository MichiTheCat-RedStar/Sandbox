# 	ai_test // ☭
# MichiTheCat-RedStar (c) 2026

from pprint import pprint

from ai_libs import Neuron, ReadTeachData, BuildVocab


# TEST
if __name__ == '__main__':
	print('Материал обучения:')
	data = ReadTeachData('dataset/synthetic_spam_train.txt')
	pprint(data)
	
	print('\nСтрою слово-число:')
	tokens = []
	for d in data:
		tokens.append(d[0])
	pprint(tokens)
	
	# NOTE: Вектор взят вообще не туда, видимо, надо стремиться к векто-
	#       рному нейрону, либо делать уже скрытый слой и целую матрицу.
