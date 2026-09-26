# 	ai_test/data/vocab // ☭
# MichiTheCat-RedStar (c) 2026


def BuildVocab(text:str) -> tuple:
	'Строит кортеж символ в id и обратно'
	
	chars = sorted(set(text))
	stoi = {c: i for i, c in enumerate(chars)}
	itos = {i: c for c, i in stoi.items()}
	return (stoi, itos)


# TODO: Функции для токенищации, векторизации и прочего
