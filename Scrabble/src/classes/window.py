import tkinter as tk
from tkinter import Frame, Label, messagebox, Button, Menu

# import os
# import matplotlib as mpl
# if os.environ.get('DISPLAY','') == '':
# 	print('no display found. Using non-interactive Agg backend')
# 	mpl.use('Agg')

class Window:
	def __init__(self, window_size: tuple, board_side:int, title: str):
		self.window = tk.Tk()
		self.window.title(title)
		self.menu_bar = Menu(self.window)
		self.window.config(menu=self.menu_bar)
		self.file_menu = Menu(self.menu_bar)
		self.file_menu.add_command(
			label='Exit game',
			command=self.window.destroy,
		)
		self.file_menu.add_command(
			label='Restart game',
			command=lambda event: self.general_click(event, 'Reinício da partida', 'Certeza que quer reiniciar a partida?', 'Dados serão apagados e partida reiniciada', 'Voltando ao jogo'),
		)
		self.menu_bar.add_cascade(
			label="File",
			menu=self.file_menu,
			underline=0
		)

		self.positions = []
		self.pack_positions = []
		self.buttons = []
		self.main_frame = Frame(self.window, width=window_size[0], height=window_size[1], relief='raised', bg="green")
		board_size = 2/3*window_size[0]
		player_height = 1/6*window_size[0]
		self.board_frame = Frame(self.main_frame, width=board_size, height=board_size, bg="blue")
		self.remote_player_frame = Frame(self.main_frame, width=window_size[0], height=player_height, bg='orange')
		self.remote_player_frame.pack(side='top')
		self.local_player_frame = Frame(self.main_frame, width=window_size[0], height=player_height, bg='orange')
		self.local_player_frame.pack(side='bottom')
		for frame in [self.board_frame, self.main_frame]:
			frame.pack()
			frame.pack_propagate(0)
		
		self.__draw_board(board_size/board_side, board_side)
		self.__draw_packs(board_size/board_side*7, 1/3*player_height,board_size/board_side)
		button = self.__draw_button('Enviar palavra', 40, 5, (20,15), self.local_player_frame)
		button.bind("<Button-1>", lambda event: self.general_click(event, 'Envio de palavra', 'Quer realmente submeter a palavra?', 'Palavra será analisada', 'Voltando ao jogo'))
		button = self.__draw_button('Retornar cards', 40, 5, (20,50), self.local_player_frame)
		button.bind("<Button-1>", lambda event: self.general_click(event, 'Retorno de cards ao pack', 'Os últimos cards adicionados ao tabuleiro serão retornados ao pack. Quer mesmo?', 'Devolvendo packs', 'Voltando ao jogo'))
		button = self.__draw_button('Passar a vez', 40, 5, (20,85), self.local_player_frame)
		button.bind("<Button-1>", lambda event: self.general_click(event, 'Passar a vez', 'Certeza que quer passar a vez?', 'Trocando de turno', 'Voltando ao jogo'))
		button = self.__draw_button('Trocar cards', 40, 5, (20, 120), self.local_player_frame)
		button.bind("<Button-1>", lambda event: self.general_click(event, 'Trocar de cards', 'Certeza que quer trocar os cards do seu pack?', 'Cards serão selecionados e a troca ocorrerá', 'Voltando ao jogo'))
		
		self.canvas = []

	#Rendering game window
	def render(self):
		self.window.mainloop()

	def __draw_board(self, position_size: int, board_side: int):
		for w in range(board_side):
			for h in range(board_side):
				x0 = w * position_size
				y0 = h * position_size
				print(x0, y0)
				new_position = Frame(self.board_frame, width=position_size, height=position_size, bg='red', highlightthickness=1, name=f'({w,h})')
				new_position.bind("<Button-1>", lambda event: self.click(event, 'Você selecionou uma posição do tabuleiro', 'Posição selecionada', 'green'))
				# new_position.bind("<Enter>", self.mouse_over)
				# new_position.bind("<Leave>", self.mouse_out)
				new_position.place(x=x0, y=y0)
				new_position.pack_propagate(0)
				self.positions.append(new_position)
				# self.canvas_board.create_rectangle(x0, y0, x1, y1, fill="blue", tags = 'border')
		
	
	def click(self, event, main_message: str, message: str, color: str):
		messagebox.showinfo(f'{main_message}', \
							f'{message}: {str(event.widget).split(".")[-1]}')
		event.widget.configure(bg=f'{color}')

	def general_click(self, event, main_message: str, ask_message: str, affirm_message: str, negat_message: str):
		answer = messagebox.askquestion(f'{main_message}', \
				  						f'{ask_message}', icon='warning')
		if answer == 'yes':
			messagebox.showinfo('', \
		       					affirm_message)
		else:
			messagebox.showinfo('', \
		       					negat_message)
	
	# def mouse_over(self, event):
	# 	event.widget.configure(bg='white')

	# def mouse_out(self, event):
	# 	event.widget.configure(bg='red')

	def __draw_packs(self, width: float, height: float, card_size: float):
		self.frame_remote_pack = Frame(self.remote_player_frame, width=width, height=height, bg="blue")
		self.frame_local_pack = Frame(self.local_player_frame, width=width, height=height, bg="blue")
		self.label_remote_player = Label(self.remote_player_frame, text="Remote player name", width=40)
		self.label_local_player = Label(self.local_player_frame, text="Local player name", width=40)
		self.label_local_player.place(x=340, y=40)
		self.label_remote_player.place(x=340, y=120)
		self.frame_remote_pack.place(x=340,y=30)
		self.frame_local_pack.place(x =340, y=90)
		for i in range(7):
			new_remote_pack_pos = Frame(self.frame_remote_pack, width=card_size, height=card_size, bg='green', highlightthickness=1, name=f'remote({0,i})')
			new_local_pack_pos = Frame(self.frame_local_pack, width=card_size, height=card_size, bg='green', highlightthickness=1, name=f'local({0,i})')
			new_local_pack_pos.bind("<Button-1>", lambda event: self.click(event, 'Você selecionou um card do pack', 'Posição do card selecionado no pack', 'red'))
			for pack_position in [new_local_pack_pos, new_remote_pack_pos]:
				pack_position.place(x=i*card_size, y=5)
				self.pack_positions.append(pack_position)

	def __draw_button(self, btn_text: str, width: float, height: float, position: tuple, main_frame: Frame) -> Button: 
		new_button = Button(main_frame, text=btn_text)
		new_button.place(x=position[0], y=position[1])
		self.buttons.append(new_button)
		return new_button