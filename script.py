import PIL
import utils
import math
import random

from utils import PI
from PIL import Image, ImageDraw

# Arranged in order of appearence in spectrum
COLORS = ['purple', 'pink', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red', 'brown' , 'darkred']

def get_coords_for_line(x, y, angle, imwidth, imheight):
	"This function helps us figure where to draw the lines"
    x_length = (x-imwidth) / math.cos(angle+180)
    y_length = (y-imheight) / math.sin(angle+180)
    length = max(abs(x_length), abs(y_length))
    endx = x + length * math.cos(math.radians(angle+180))
    endy = y + length * math.sin(math.radians(angle+180))

    return endx, endy

def render(img, digits, method = 'twotone'):
	x, y = img.width // 2, img.height //2
	draw = ImageDraw.Draw(img)

	for i in range(digits):
		n = int(PI[i])
		if method == 'all':
			color = COLORS[n]
		elif method == 'twotone':
			color = COLORS[n%2]

		a, b = get_coords_for_line(x, y, math.degrees(max(1, n) + i) , 0, 0)
		draw.line(((x, y), (a, b)), fill= color, width=7)

	return img

def save(img, fp, resize = False, resize_dimension = None):
	if resize:
		img = img.resize(resize_dimension, resample = Image.BOX)
	img.save(fp)
	return img

def main():
	img = Image.new('RGB', (4096, 4096), color = 'black')

	# SET method TO 'all' for all colors and 'twotone' for 2 colors.
	# Change digit to control the number of lines in image/digits in pi.
	img = render(img, digits= 1000, method= 'twotone')
	save(img, 'output.png')

if __name__ == '__main__':
	main()