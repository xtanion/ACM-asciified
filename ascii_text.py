import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont

Character = {
    "standard": "@%#*+=-:. ",
    "inverse": " .:-=+*#%@",
    "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}


def get_data(mode):
    font = ImageFont.truetype("fonts/DejaVuSansMono-Bold.ttf", size=18)
    scale = 2
    char_list = Character[mode]
    return char_list, font, scale


bg_color = 0
char_list, font, scale = get_data(mode = 'standard')
num_chars = len(char_list)
num_cols = 100


def read_image(path):
    if os.path.exists(path):        
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    else:
        print('Image doesnot exists!! please check path')
        return None


def generate_ascii_image(image, fname='output.png'):
    
    height, width = image.shape
    cell_width = width / num_cols
    cell_height = scale * cell_width
    num_rows = int(height / cell_height)
    char_width, char_height = font.getsize("A")
    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows

    out_image = Image.new("L", (out_width, out_height), bg_color)
    draw = ImageDraw.Draw(out_image)
    
    for i in range(num_rows):

        chars = []

        for j in range(num_cols):
            min_cell_height = min(int((i + 1) * cell_height), height)
            min_cell_width = min(int((j + 1) * cell_width), width)
            
            elem = image[int(i * cell_height):min_cell_height, int(j * cell_width):min_cell_width]
            p = np.mean(elem) / 255 * num_chars
            t = min(int(p), num_chars - 1)
            
            chars.append(char_list[t])
        
        line = f'{"".join(chars)}\n'
        draw.text((0, i * char_height), line, fill = 255, font=font)


    cropped_image = out_image.getbbox()
    out_image = out_image.crop(cropped_image)
    out_image.save(fname)

def main():
    image_path = 'data/meme_cat.png'
    image = read_image(image_path)
    generate_ascii_image(image, 'tmp/ascii_out.png')

# to run the code -->
main()
