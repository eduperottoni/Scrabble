from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from dog.start_status import StartStatus
import tkinter as tk
from tkinter import Frame, Label, messagebox, Button, Menu, Canvas, simpledialog, PhotoImage
from PIL import Image, ImageTk

class PlayerInterface(DogPlayerInterface):
	def __init__(self, window_size: tuple, board_side:int, title: str):
		self.window = tk.Tk()
		self.window.title(title)
		self.menu_bar = Menu(self.window)
		self.window.config(menu=self.menu_bar)
		self.file_menu = Menu(self.menu_bar)
		self.file_menu.add_command(
			label='Start game',
			command=self.start_game
		)
		self.file_menu.add_command(
			label='Exit game',
			command=self.window.destroy,
		)
		self.file_menu.add_command(
			label='Restart game',
			command= self.window.destroy,
		)
		self.menu_bar.add_cascade(
			label="Game options",
			menu=self.file_menu,
			underline=0
		)
		self.positions = []
		self.pack_positions = []
		self.buttons = []
		self.cards = []
		self.scores = []
		self.main_frame = Frame(self.window, width=window_size[0], height=window_size[1], relief='raised', bg="green")
		board_size = 2/3*window_size[0]
		player_height = 1/6*window_size[0]
		self.board_frame = Frame(self.main_frame, width=board_size, height=board_size, bg="blue")
		self.remote_player_frame = Frame(self.main_frame, width=window_size[0], height=player_height, bg='orange')
		self.remote_player_frame.pack(side='top')
		self.scores.append(self.__draw_score(self.remote_player_frame, (200,100), (720, 30)))
		self.local_player_frame = Frame(self.main_frame, width=window_size[0], height=player_height, bg='orange')
		self.local_player_frame.pack(side='bottom')
		self.scores.append(self.__draw_score(self.local_player_frame, (200,100), (720, 30)))
		for frame in [self.board_frame, self.main_frame]:
			frame.pack()
			frame.pack_propagate(0)
		self.__draw_board(board_size/board_side, board_side)
		self.__draw_packs((board_size/board_side*7, 1/3*player_height), board_size/board_side)
		button = self.__draw_button('Enviar palavra', 40, 5, (20,15), self.local_player_frame)
		button.bind("<Button-1>", lambda event: self.general_click(event, 'Envio de palavra', 'Quer realmente submeter a palavra?', 'Palavra será analisada', 'Voltando ao jogo'))
		button = self.__draw_button('Retornar cards', 40, 5, (20,50), self.local_player_frame)
		button.bind("<Button-1>", lambda event: self.general_click(event, 'Retorno de cards ao pack', 'Os últimos cards adicionados ao tabuleiro serão retornados ao pack. Quer mesmo?', 'Devolvendo packs', 'Voltando ao jogo'))
		button = self.__draw_button('Passar a vez', 40, 5, (20,85), self.local_player_frame)
		button.bind("<Button-1>", lambda event: self.general_click(event, 'Passar a vez', 'Certeza que quer passar a vez?', 'Trocando de turno', 'Voltando ao jogo'))
		button = self.__draw_button('Trocar cards', 40, 5, (20, 120), self.local_player_frame)
		button.bind("<Button-1>", lambda event: self.general_click(event, 'Trocar de cards', 'Certeza que quer trocar os cards do seu pack?', 'Cards serão selecionados e a troca ocorrerá', 'Voltando ao jogo'))
		self.__render()

	#Rendering game window
	def __render(self):
		self.__initialize_dog()
		self.window.mainloop()

	def __initialize_dog(self):
		player_name = simpledialog.askstring(title='Identificação de jogador', prompt='Digite o seu nome:')
		self.dog_server_interface = DogActor()
		message = self.dog_server_interface.initialize(player_name, self)
		messagebox.showinfo(message=message)


	# drawing the 255 positions of the board
	def __draw_board(self, position_size: int, board_side: int):
		dw = [(1,1), (2,2), (3,3), (4,4), (13,13), (12,12), (11,11), (10,10), (1,13), (2,12), (3,11), (4,10), (13,1), (12,2), (11,3), (10,4)]
		dl = [(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8,12), (11,0), (11,7), (11,14), (12,6), (12,8), (13,3), (13,11)]
		tl = [(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13,5), (13,9)]
		# for line in range(board_side):
		# 	new_list = []
		# 	for column in range(board_side):
		# 		x0 = column * position_size
		# 		y0 = line * position_size
		# 		new_position = Frame(self.board_frame, width=position_size, height=position_size, bg='gray', highlightthickness=1, name=f'({line, column})')
		# 		new_canvas = Canvas(new_position, width=position_size-2, height=position_size-2, name=f'({line, column})')
		# 		color = 'gray'
		# 		#drawing special positions
		# 		if (line in [0, 7, 14] and column in [0, 7, 14] and (line, column) != (7,7)):
		# 			new_canvas.place(x=-1, y=-1)
		# 			color='orange'
		# 			new_canvas.create_text(20,20, text='TW', font=('Arial', 16))
		# 		elif ((line, column) in dw):
		# 			new_canvas.place(x=-1, y=-1)
		# 			color='yellow'
		# 			new_canvas.create_text(20,20, text='DW', font=('Arial', 16))
		# 		elif ((line, column) in dl):
		# 			new_canvas.place(x=-1, y=-1)
		# 			color='blue'
		# 			new_canvas.create_text(20,20, text='DL', font=('Arial', 16))
		# 		elif ((line, column) in tl):
		# 			new_canvas.place(x=-1, y=-1)
		# 			color='purple'
		# 			new_canvas.create_text(20,20, text='TL', font=('arial', 16))
		# 		elif ((line, column) == (7,7)):
		# 			new_canvas.place(x=-1, y=-1)
		# 			color='black'
		# 			new_canvas.create_text(20,20, text='#', font=('Arial', 16), fill='white')
	 
		# 		new_canvas.configure(bg=f'{color}')
		# 		new_canvas.bind("<Button-1>", lambda event: self.click(event, 'Você selecionou uma posição do tabuleiro', 'Posição selecionada', 'green'))
		# 		new_position.bind("<Button-1>", lambda event: self.click(event, 'Você selecionou uma posição do tabuleiro', 'Posição selecionada', 'green'))
		# 		new_position.place(x=x0, y=y0)
		# 		new_position.pack_propagate(0)
		# 		new_list.append(new_position)
		# 	self.positions.append(new_list)
		
		image_pil = Image.open('src/images/positions/scrabble_DW.png')
		RESIZED = image_pil.resize((int(position_size), int(position_size)), Image.ANTIALIAS)
		tk_image = ImageTk.PhotoImage(RESIZED)
		label_image = Label(self.board_frame, bd=0, image=tk_image)
		label_image.image = tk_image
		label_image.pack()
		label_image.bind('<Button-1>', lambda event: self.click(event, 'Você selecionou uma posição do tabuleiro', 'Posição selecionada', 'green'))
		# new_canvas.place(x=-1, y=-1)
		color='orange'

	#click event in positions of the board
	def click(self, event, main_message: str, message: str, color: str):
		messagebox.showinfo(f'{main_message}', \
							f'{message}: {(str(event.widget)).split(".")[-1]}')
		event.widget.configure(bg=f'{color}')

	#click event in the buttons
	def general_click(self, event, main_message: str, ask_message: str, affirm_message: str, negat_message: str):
		answer = messagebox.askquestion(f'{main_message}', \
				  						f'{ask_message}', icon='warning')
		if answer == 'yes':
			messagebox.showinfo('', \
		       					affirm_message)
		else:
			messagebox.showinfo('', \
		       					negat_message)

	def __askquestion(self, title: str, ask_message: str) -> None:
		answer = messagebox.askquestion(title, ask_message, icon='question')
		return True if answer == 'yes' else False
	
	def __show_message(self, title: str, message: str) -> None:
		messagebox.showinfo(title=title, message=message)

	#Drawing packs
	def __draw_packs(self, pack_size: tuple, card_size: float):
		self.frame_remote_pack = Frame(self.remote_player_frame, width=pack_size[0], height=pack_size[1], bg="blue")
		self.frame_local_pack = Frame(self.local_player_frame, width=pack_size[0], height=pack_size[1], bg="blue")
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
			card = self.__draw_card(new_local_pack_pos, (card_size, card_size), 'A', 8)
			self.cards.append(card)

	#Drawing buttons
	def __draw_button(self, btn_text: str, width: float, height: float, position: tuple, main_frame: Frame) -> Button: 
		new_button = Button(main_frame, text=btn_text)
		new_button.place(x=position[0], y=position[1])
		self.buttons.append(new_button)
		return new_button
	
	#draw card (using Canvas widget)
	def __draw_card(self, main_frame: Frame, size: tuple, letter: str, value: int) -> Canvas:
		card = Canvas(main_frame, width=size[0], height=size[1], bg='green', name=f'{main_frame.winfo_name()}')
		card.place(x=0,y=0)
		card.create_text(16, 16, text=f'{letter}', font=('Arial', 16))
		card.create_text(size[0] - 10, size[1] - 10, text=f'{value}', font=('Arial', 8))
		card.bind("<Button-1>", lambda event: self.click(event, 'Você selecionou um card do pack', 'Posição do card selecionado no pack', 'red'))
		return card
	
	#Drawing scores (using Canvas widget)
	def __draw_score(self, main_frame: Frame, size: tuple, position: tuple) -> Canvas:
		new_score = Canvas(main_frame, width=size[0], height=size[1], bg='blue')
		new_score.create_text(100, 16, text="PONTUAÇÃO", font=('Arial', 16))
		new_score.place(x=position[0], y=position[1])
		return new_score
	
	#Starting game (com o DOG)
	def start_game(self) -> None:
		self.__show_message('Início do jogo', 'O jogo será iniciado')
		start_status = self.dog_server_interface.start_match(2)
		message = start_status.get_message()
		self.__show_message(title='Mensagem do DOG', message=message)

	#Receiving game's start from DOG
	def receive_start(self, start_status: StartStatus) -> None:
		message = start_status.get_message()
		self.__show_message(title='Mensagem do DOG', message=message)