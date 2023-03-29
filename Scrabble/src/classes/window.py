import tkinter as tk
from tkinter import Frame, Label


class Window:
	def __init__(self, window_size: tuple, title: str):
		self.window = tk.Tk()
		self.window.resizable(False, False)
		self.window.title(title)

		self.main_frame = Frame(self.window, width=window_size[0], height=window_size[1], relief='raised', bg="green")
		board_size = 2/3*window_size[0]
		self.board_frame = Frame(self.main_frame, width=board_size, height=board_size, bg="blue")
		
		
		
		# self.frame_baixo = Frame(self.main_frame,width=450, height=200, bg='orange')
		# self.label1 = Label(self.frame_meio, text='To no frame de cima!')
		# self.label2 = Label(self.frame_baixo, text='To no frame de baixo!')

		# self.label1.pack(side='top')
		# self.label2.pack(side='top')
		
		for frame in [self.board_frame, self.main_frame]:
			frame.pack()
			frame.pack_propagate(0)
		self.board_frame.bind("<Button-1>", self.func)
		# self.frame_meio.pack()

		self.canvas = []



		# self.canvas = tk.Canvas(self.main, width=self.canvas_size[0], height=canvas_size[1])
		
		# self.canvas_window.pack()
		# self.canvas_board = tk.Canvas(self.canvas_window, width=300, height=300)
		# self.canvas_board.place(x=50,y=50)
		# self.canvas_board.pack();

	#Rendering game window
	def render(self):
		self.window.mainloop()

	def draw_board(self, position_size: int, board_side: int):
		for w in range(board_side):
			for h in range(board_side):
				x0 = w * position_size
				y0 = h * position_size
				x1 = x0 + position_size
				y1 = y0 + position_size
				new_canvas = tk.Canvas(self.frame_meio, width=position_size, height=position_size)
				new_canvas.create_rectangle(0,0,position_size, position_size, fill="blue", tags='border')
				new_canvas.place(x=x0, y=y0)
				new_canvas.bind("<Button-1>", self.func)
				self.canvas.append(new_canvas)
				new_canvas.pack()
				# self.canvas_board.create_rectangle(x0, y0, x1, y1, fill="blue", tags = 'border')
		
	
	def func(self, event):
		print("Oi", event.x, event.y)

		

		# for i in range(15):
		# 	for j in range(15):
		# 		self.canvas.create_rectangle((25*i+12, 25*j+12, 25*i+37, 25*j+37), width=4.0,
		# 										fill="brown", tags="border")
		# for i in [1, 2, 3, 4, 10, 11, 12, 13]:
		# 	self.canvas.create_text((25*i + 25, 25*i + 25), text='2W ', tags="board")
		# 	self.canvas.create_text((25*i + 25, 25*(14-i) + 25), text='2W ', tags="board")
		# 	self.canvas.create_text((200,200), text='2W ', tags="board")
		# 	self.canvas.create_text((25, 25), text='3W ', tags="board")
		# 	self.canvas.create_text((25, 200), text='3W ', tags="board")
		# 	self.canvas.create_text((200, 25), text='3W ', tags="board")
		# 	self.canvas.create_text((25, 375), text='3W ', tags="board")
		# 	self.canvas.create_text((375, 25), text='3W ', tags="board")
		# 	self.canvas.create_text((200,375), text='3W ', tags="board")
		# 	self.canvas.create_text((375,200), text='3W ', tags="board")
		# 	self.canvas.create_text((375, 375), text='3W ', tags="board")

		# 	self.canvas.create_text((100, 25), text='2L ', tags="board")
		# 	self.canvas.create_text((175, 75), text='2L ', tags="board")
		# 	self.canvas.create_text((25, 100), text='2L ', tags="board")
		# 	self.canvas.create_text((200,100), text='2L ', tags="board")
		# 	self.canvas.create_text((75,175), text='2L ', tags="board")
		# 	self.canvas.create_text((100,200), text='2L ', tags="board")
		# 	self.canvas.create_text((175, 175), text='2L ', tags="board")

		# 	self.canvas.create_text((300,25), text='2L ', tags="board")
		# 	self.canvas.create_text((225,75), text='2L ', tags="board")
		# 	self.canvas.create_text((375, 100), text='2L ', tags="board")
		# 	self.canvas.create_text((225, 175), text='2L ', tags="board")
		# 	self.canvas.create_text((325, 175), text='2L ', tags="board")
		# 	self.canvas.create_text((300, 200), text='2L ', tags="board")

		# 	self.canvas.create_text((100, 375), text='2L ', tags="board")
		# 	self.canvas.create_text((175, 325), text='2L ', tags="board")
		# 	self.canvas.create_text((25, 300), text='2L ', tags="board")
		# 	self.canvas.create_text((75, 225), text='2L ', tags="board")
		# 	self.canvas.create_text((175, 225), text='2L ', tags="board")
		# 	self.canvas.create_text((200, 300), text='2L ', tags="board")

		# 	self.canvas.create_text((300, 375), text='2L ', tags="board")
		# 	self.canvas.create_text((225, 325), text='2L ', tags="board")
		# 	self.canvas.create_text((375, 300), text='2L ', tags="board")
		# 	self.canvas.create_text((325, 225), text='2L ', tags="board")
		# 	self.canvas.create_text((225, 225), text='2L ', tags="board")

		# 	self.canvas.create_text((150,50), text='3L ', tags="board")
		# 	self.canvas.create_text((50,150), text='3L ', tags="board")
		# 	self.canvas.create_text((150,150), text='3L ', tags="board")

		# 	self.canvas.create_text((250,50), text='3L ', tags="board")
		# 	self.canvas.create_text((250,150), text='3L ', tags="board")
		# 	self.canvas.create_text((350,150), text='3L ', tags="board")

		# 	self.canvas.create_text((250, 350), text='3L ', tags="board")
		# 	self.canvas.create_text((350,250), text='3L ', tags="board")
		# 	self.canvas.create_text((250,250), text='3L ', tags="board")

		# 	self.canvas.create_text((50,250), text='3L ', tags="board")
		# 	self.canvas.create_text((150,250), text='3L ', tags="board")
		# 	self.canvas.create_text((150,350), text='3L ', tags="board")

