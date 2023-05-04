from PIL import Image, ImageDraw, ImageFont

#Path to save the positions
PATH = 'positions'

# Define constants for the size and layout of the position
POSITION_WIDTH = 225
POSITION_HEIGHT = 225
BORDER_WIDTH = 10
LETTER_SIZE = 140
LETTER_FONT = ImageFont.truetype('../fonts/Roboto-Medium.ttf', LETTER_SIZE)

# Define the colors for the position background and border
POSITION_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)

# Define a positions list
POSITIONS = ['DW', 'TL', 'DW', 'TW', '*', 'NORMAL']

# Define a function to draw a position for a given description
def draw_card(pos_desc: str) -> None:
    # Create a new image for the position
    position = Image.new('RGB', (POSITION_WIDTH, POSITION_HEIGHT), POSITION_COLOR)
    draw = ImageDraw.Draw(position)
    
    # Draw the description in the center of the position
    if (pos_desc != 'NORMAL'):
        letter_width, letter_height = draw.textsize(pos_desc, font=LETTER_FONT)
        x = (POSITION_WIDTH - letter_width) / 2
        y = (POSITION_HEIGHT - letter_height) / 2
        draw.text((x, y), pos_desc, fill=BORDER_COLOR, font=LETTER_FONT)
    
    # Draw a border around the position
    draw.rectangle((0, 0, POSITION_WIDTH - 1, POSITION_HEIGHT - 1), outline=BORDER_COLOR, width=BORDER_WIDTH)
    
    filename = f'scrabble_{pos_desc}.png'
    position.save(f'{PATH}/{filename}')
    print(f'File {PATH}/{filename} saved')

    # return position

for description in POSITIONS:
    card = draw_card(description)
