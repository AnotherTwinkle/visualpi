import PIL
import utils
import math
import random

from utils import PI, PHI, E
from PIL import Image, ImageDraw

# Arranged in order of appearence in spectrum
COLORS = ['purple', 'pink', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red', 'brown' , 'darkred']

def get_coords_for_line(x, y, angle, imwidth, imheight):
	"""This function helps us figure where to draw the lines"""
	angle = (360 - angle) or 360

	x_length = (x-imwidth) / math.cos(angle)
	y_length = (y-imheight) / math.sin(angle)
	length = max(abs(x_length), abs(y_length))
	endx = x + length * math.cos(math.radians(angle))
	endy = y + length * math.sin(math.radians(angle))
	return endx, endy

def render(img, digits, constant, method = 'twotone'):
	x, y = img.width // 2, img.height //2
	draw = ImageDraw.Draw(img)
	sum_value = 0

	for i in range(digits):
		n = int(constant[i])
		sum_value += n 
		rad = sum_value / (i + 1) # Calculate the running average for the i-th digit of pi

		if method == 'all':
			color = COLORS[n]
		elif method == 'twotone':
			color = COLORS[n%2]
		elif method == 'swap':
			color = COLORS[i//1000]

		a, b = get_coords_for_line(x, y, math.degrees(rad), 0, 0)
		draw.line(((x, y), (a, b)), fill= color, width= 3)

	print(sum_value/digits)
	return img

def save(img, fp, resize = False, resize_dimension = None):
	if resize:
		img = img.resize(resize_dimension, resample = Image.BOX)
	img.save(fp)
	return img


def main():
	img = Image.new('RGB', (4096, 4096), color = 'black')

	# SET method TO 'all' for all colors and 'twotone' for 2 colors.
	# SET method TO 'swap' for swapping colors every 1k digits.
	# Change digit to control the number of lines in image/digits in pi\
	img = render(img, digits= 10000, constant= PI, method= 'swap')
	save(img, 'output.png')

if __name__ == '__main__':
	main()