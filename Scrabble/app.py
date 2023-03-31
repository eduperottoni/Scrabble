from src.classes.player_interface import PlayerInterface

interface = PlayerInterface((960, 960), 15, "Scrabble")
interface.render()


# import tkinter as tk
# from PIL import Image, ImageTk
# import random

# # Criando a janela principal
# root = tk.Tk()
# root.title("Scrabble")

# # Criando as variáveis para a pontuação e as peças dos jogadores
# score1 = tk.IntVar()
# score2 = tk.IntVar()
# tiles1 = tk.StringVar()
# tiles2 = tk.StringVar()

# # Inicializando as peças dos jogadores com letras aleatórias
# alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# tiles1.set(''.join(random.sample(alphabet, 7)))
# tiles2.set(''.join(random.sample(alphabet, 7)))

# # Função para atualizar as peças dos jogadores
# def update_tiles():
#     tiles1.set(''.join(random.sample(alphabet, 7)))
#     tiles2.set(''.join(random.sample(alphabet, 7)))

# # Criando as labels para exibir a pontuação e as peças dos jogadores
# player1_label = tk.Label(root, text="Jogador 1")
# player1_score_label = tk.Label(root, textvariable=score1)
# player1_tiles_label = tk.Label(root, textvariable=tiles1)

# player2_label = tk.Label(root, text="Jogador 2")
# player2_score_label = tk.Label(root, textvariable=score2)
# player2_tiles_label = tk.Label(root, textvariable=tiles2)

# # Criando o botão para atualizar as peças dos jogadores
# update_button = tk.Button(root, text="Trocar peças", command=update_tiles)

# # Carregando as imagens das cartas
# card_images = {}
# for i in range(1, 8):
#     card_images[str(i)] = ImageTk.PhotoImage(Image.open(f"cards/{i}.png"))
#     card_images[str(i) + "w"] = ImageTk.PhotoImage(Image.open(f"cards/{i}w.png"))

# # Criando o canvas para desenhar o tabuleiro
# canvas_width = 700
# canvas_height = 700
# canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
# canvas.pack()

# # Desenhando o tabuleiro
# for row in range(15):
#     for col in range(15):
#         x1 = col * 40
#         y1 = row * 40
#         x2 = x1 + 40
#         y2 = y1 + 40
#         canvas.create_rectangle(x1, y1, x2, y2, fill="light blue")

# # Desenhando as cartas dos jogadores
# for i, letter in enumerate(tiles1.get()):
#     x = 550 + i * 60
#     y = 600
#     canvas.create_image(x, y, image=card_images[letter])
# for i, letter in enumerate(tiles2.get()):
#     x = 550 + i * 60
#     y = 50
#     canvas.create_image(x, y, image=card_images[letter])

# # Posicionando os widgets na janela principal
# player1_label.grid(row=0, column=0)
# player1_score_label.grid(row=1, column=0)
# player1_tiles_label.grid(row=2, column=0)

# player2_label.grid(row=0, column=2)
# player2_score_label.grid(row=1, column=2)
# player2_tiles_label.grid(row=2, column=2)

# update_button.grid(row=3, column=1)

# # Iniciando o loop principal da interface gráfica
# root.mainloop()