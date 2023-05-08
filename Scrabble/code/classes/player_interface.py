from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from dog.start_status import StartStatus
import tkinter as tk
from tkinter import Frame, Label, messagebox, Button, Menu, Canvas, simpledialog, PhotoImage
from PIL import Image, ImageTk

from classes.round_manager import RoundManager
from classes.enums import State
from constants import messages
class PlayerInterface(DogPlayerInterface):
	def __init__(self, window_size: tuple, board_side:int, title: str):
		self.round_manager = RoundManager()
		self.window_size = window_size
		self.board_side = board_side
		self.board_size = 2/3 * window_size[0]
		self.title = title
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
		print('Cheguei aqui')
		self.file_menu.add_command(
			label='Restart game',
			command= self.window.destroy,
		)
		self.menu_bar.add_cascade(
			label="Game options",
			menu=self.file_menu,
			underline=0
		)
		# Matrix of labels
		self.board_positions = []
		# List of labels
		self.pack_positions = []
		self.buttons = {
			'button(submit)': {'btn_description': 'Submeter palavra',
		      				   'btn_position': (20,15)},
			'button(return)': {'btn_description': 'Retornar cards', 
		      				   'btn_position': (20,50)},
			'button(giveup)': {'btn_description': 'Passar a vez',
		    				   'btn_position': (20,85)},
			'button(change)': {'btn_description': 'Trocar cards',
		      				   'btn_position': (20,120)}
		}
		self.cards = []
		self.scores = []
		self.main_frame = Frame(self.window, width=window_size[0], height=window_size[1], relief='raised', bg="green")
		player_height = 1/6*window_size[0]
		self.board_frame = Frame(self.main_frame, width=self.board_size, height=self.board_size, bg="blue")
		self.remote_player_frame = Frame(self.main_frame, width=window_size[0], height=player_height, bg='orange')
		self.remote_player_frame.pack(side='top')
		self.scores.append(self.__draw_score(self.remote_player_frame, (200,100), (720, 30)))
		self.local_player_frame = Frame(self.main_frame, width=window_size[0], height=player_height, bg='orange')
		self.local_player_frame.pack(side='bottom')
		self.scores.append(self.__draw_score(self.local_player_frame, (200,100), (720, 30)))
		for frame in [self.board_frame, self.main_frame]:
			frame.pack()
			frame.pack_propagate(0)
		self.__draw_packs((self.board_size/board_side*7, 1/3*player_height), self.board_size/board_side)
		self.__render_gui()

	#Rendering game window
	def __render_gui(self):
		self.__initialize_dog()
		self.__draw_board(self.board_size/self.board_side, self.board_side)
		self.__draw_buttons()
		self.window.mainloop()

	def __initialize_dog(self):
		player_name = simpledialog.askstring(title='Identificação de jogador', prompt='Digite o seu nome:')
		self.dog_server_interface = DogActor()
		message = self.dog_server_interface.initialize(player_name, self)
		messagebox.showinfo(message=message)

	def __activate_user_actions(self):
		for button in self.buttons.keys():
			if button == 'button(submit)':
				button.bind(
					"<Button-1>",
					lambda event: self.general_click(
						event, 
						'Envio de palavra',
						'Quer realmente submeter a palavra?',
						'Palavra será analisada', 'Voltando ao jogo'))
			elif button == 'button(return)':
				button.bind(
					"<Button-1>",
					lambda event: self.general_click(
						event,
						'Retorno de cards ao pack',
						'Os últimos cards adicionados ao tabuleiro serão retornados ao pack. Quer mesmo?',
						'Devolvendo packs', 'Voltando ao jogo'))
			elif button == 'button(giveup)':
				button.bind(
					"<Button-1>",
					lambda event: self.general_click(event,
				      'Passar a vez', 'Certeza que quer passar a vez?',
					  'Trocando de turno', 'Voltando ao jogo'))
			elif button == 'button(change)':
				button.bind(
					"<Button-1>",
					lambda event: self.general_click(event,
				      'Trocar de cards', 'Certeza que quer trocar os cards do seu pack?',
					  'Cards serão selecionados e a troca ocorrerá', 'Voltando ao jogo'))
		for label in self.board_positions:
			label.bind(
				'<Button-1>',
				lambda event: self.click(
					event,
					'Você selecionou uma posição do tabuleiro', 
					'Posição selecionada', 'green')
			)

	#Drawing button
	def __draw_button(self, btn_text: str, width: float, height: float, position: tuple, main_frame: Frame, name: str) -> Button: 
		new_button = Button(main_frame, text=btn_text, name=name)
		new_button.place(x=position[0], y=position[1])
		return new_button
	
	def __draw_buttons(self):
		for button_name, button_config in self.buttons.items():
			button = self.__draw_button(button_config['btn_description'], None, None, button_config['btn_position'], self.local_player_frame, button_name)
			self.buttons[button_name]['btn_object'] = button
	
	# drawing the 255 positions of the board
	def __draw_board(self, position_size: int, board_side: int):
		RELATIVE_PATH = 'src/images/positions/scrabble'
		POSITIONS_IMG_DICT = {
			'DW' : f'{RELATIVE_PATH}_DW.png',
			'DL' : f'{RELATIVE_PATH}_DL.png',
			'TW' : f'{RELATIVE_PATH}_TW.png',
			'TL' : f'{RELATIVE_PATH}_TL.png',
			'NORMAL' : f'{RELATIVE_PATH}_NORMAL.png',
			'*' : f'{RELATIVE_PATH}_*.png'
		}
		
		tw = [(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)]
		dw = [(1,1), (2,2), (3,3), (4,4), (13,13), (12,12), (11,11), (10,10), (1,13), (2,12), (3,11), (4,10), (13,1), (12,2), (11,3), (10,4)]
		dl = [(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8,12), (11,0), (11,7), (11,14), (12,6), (12,8), (14,3), (14,11)]
		tl = [(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13,5), (13,9)]
		
		for line in range(board_side):
			positions_line = []
			for column in range(board_side):
				# Defining positions
				x0 = column * position_size
				y0 = line * position_size
				frame_position = Frame(self.board_frame, width=position_size, height=position_size, bg='gray', highlightthickness=1)
				
				# We create the Label's image depending on the type o the position
				dict_key = 'NORMAL'
				if ((line, column) in tw):
					dict_key = 'TW'
				elif ((line, column) in dw):
					dict_key = 'DW'
				elif ((line, column) in dl):
					dict_key = 'DL'
				elif ((line, column) in tl):
					dict_key = 'TL'
				elif ((line, column) == (7,7)):
					dict_key = '*'
				
				# Creating Label's image
				pil_img = Image.open(POSITIONS_IMG_DICT[dict_key])
				resized_img = pil_img.resize((int(position_size)-6, int(position_size)-6), Image.ANTIALIAS)
				tk_img = ImageTk.PhotoImage(resized_img)
				label_img = Label(
					frame_position, 
					bg='white', 
					image=tk_img, 
					borderwidth=3,
					name=f'board({line, column})'
				)
				label_img.image = tk_img
				label_img.pack()
				frame_position.place(x=x0, y=y0)

				# Iserting label on line
				positions_line.append(label_img)

			# Iserting line on positions matrix
			self.board_positions.append(positions_line)
	
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
		#TODO Inserir validação de estado do jogo
		# Se o estado do jogo estiver em NOT_INITIALIZED
		if (self.round_manager.match_state == State.NOT_INITIALIZED):
			print('ESTADO DO JOGO É VÁLIDO PARA SEU INÍCIO')
			answer = self.__askquestion(messages.START_MATCH_TITLE, messages.START_MACTH_QUESTION)
			if answer:
				print('ENVIANDO PEDIDO DE INÍCIO DO JOGO AO SERVIDOR')
				start_status = self.dog_server_interface.start_match(2)
				code = start_status.get_code()
				message = start_status.get_message()
				if code == '0' or code == '1':
					self.__show_message(messages.START_MATCH_DOG_RESPONSE_TITLE, message)
				else:
					players_response = start_status.get_players()
					# Building player dict and order list to pass as parameter in RoundManager.start_match()
					players = {'local': 
								{'id': players_response[0][1],
	 							'name': players_response[0][0],
								'turn': True if players_response[0][2] == 1 else False},
							   'remote':
							   	{'id': players_response[1][1],
	    						'name': players_response[1][0],
								'turn': True if players_response[1][2] == 1 else False}
							}
					print('2 JOGADORES ENCONTRADOS PARA INÍCIO DO JOGO')
					self.round_manager.start_game(players)
					#TODO Chamar a ativação da ação do usuário para ações nos widgets da interface
					self.__show_message(messages.START_MATCH_DOG_RESPONSE_TITLE, message)



	#Receiving game's start from DOG
	def receive_start(self, start_status: StartStatus) -> None:
		message = start_status.get_message()
		self.__show_message(title='Mensagem do DOG', message=message)