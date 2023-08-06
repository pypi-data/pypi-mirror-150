import colorama

def color_print(*args, color):
	text = ""
	for i in args:
		text += i
	if color == "green":
		print(colorama.Fore.GREEN + text)

if __name__ == "__main__":
	color_print("hello world!", color="green")