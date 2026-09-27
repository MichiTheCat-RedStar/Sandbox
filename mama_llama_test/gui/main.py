# 	mama_llama_test // ☭
# MichiTheCat-RedStar (c) 2026

print('mama_llama_test - MichiTheCat-RedStar (c) 2026.')
print('Интерфейс для Ollama под Linux...\n')


# Импорт модулей
print('Попытка импорта ollama...', end='', flush=True)
try: from ollama import chat
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта tkinter...', end='', flush=True)
try: import tkinter
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта threading...', end='', flush=True)
try: from threading import Thread
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')

print('Попытка импорта time...', end='', flush=True)
try: from time import time
except ModuleNotFoundError: print('\b'*3, '[Неудачно!]\n'); raise
else: print('\b'*3, '[Успешно.]')


# Основной код
def Send():
	ai_text.set('Думаю...')
	Thread(target=_Worker, daemon=True).start()


def _Worker():
	prompt = input_text.get('1.0', 'end-1c')
	print('Пользователь:\n'+prompt)
	start = time()
	try:
		response = chat(model='smollm2:360m-instruct-q8_0', messages=[{'role': 'user', 'content': prompt}])
		ai_text.set(response['message']['content'])
	except Exception as e:
		ai_text.set(f'Ошибка: {e}')
	print('\nИИ:\n'+response['message']['content'])
	print('\nДумал:', round(time()-start), 'секунд')


# Точка входа
if __name__ == '__main__':
	print('\nИнициализация...\n')
	
	root = tkinter.Tk()
	root.title('Ollama Tkinter GUI from MichiTheCat-RedStar')
	root.geometry("400x300")
	root.resizable(True, True)
	
	ai_text = tkinter.StringVar(value='Введите свой первый запрос...')
	
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)
	
	output_text = tkinter.Label(root, textvariable=ai_text, bg='#a0a0a0', anchor='nw', wraplength=400)
	output_text.grid(row=0, column=0, columnspan=2, sticky="nsew")
	
	input_text = tkinter.Text(root, height=10, width=40, bd=3)
	input_text.grid(row=1, column=0, sticky="nsew")
	
	input_button = tkinter.Button(root, text='send', command=Send, bg='#E60C0C')
	input_button.grid(row=1, column=1, sticky="nsew")
	
	root.mainloop()
	
	#TODO: Использовать Text вместо Label и улучшить GUI (я не фронт :з) 
