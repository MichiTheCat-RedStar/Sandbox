# 	ai_test/io/saves // ☭
# MichiTheCat-RedStar (c) 2026


from pathlib import Path


def SaveW(layer, file_path:bool|str=False):
	'Сохранение весов для слоёв (Layer)'
	
	if file_path:
		p = Path(file_path)
	else:
		p = Path('saves/'+file_path)
	
	...
	#TODO: Имя файла, доделать функцию, я умираю от желания спать



def LoadW(layer, file_path:str) -> list[float]:
	'Загрузка весов для слоёв (Layer)'
	...
