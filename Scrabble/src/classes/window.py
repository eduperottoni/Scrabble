import tkinter as tk


class Window:
	def __init__(self, canvas_size: tuple, title: str):
		self.canvas_size = canvas_size
		self.main = tk.Tk()
		self.main.title(title)
		self.canvas = tk.Canvas(self.main, width=self.canvas_size[0], height=canvas_size[1])
		self.canvas.pack()

	#Rendering game window
	def render(self):
		self.main.mainloop()

	def draw_board(self, position_size: int, board_side: int):
		for w in range(board_side):
			for h in range(board_side):
				x0 = w * position_size
				y0 = h * position_size
				x1 = x0 + position_size
				y1 = y0 + position_size
				self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline = 'black')

