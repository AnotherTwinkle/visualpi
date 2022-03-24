import PIL
import utils
import math

from utils import PI, PHI, E
from PIL import Image, ImageDraw

# Arranged in order of appearence in spectrum
COLORS = ['purple', 'pink', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red', 'brown' , 'darkred']

def get_coords_for_line(x, y, angle, imwidth, imheight):
	angle = 360 - angle; angle = 360 if angle == 0 else angle

	x_length = (x-imwidth) / math.cos(angle)
	y_length = (y-imheight) / math.sin(angle)
	length = max(abs(x_length), abs(y_length))
	endx = x + length * math.cos(math.radians(angle))
	endy = y + length * math.sin(math.radians(angle))
	return endx, endy

class ColorMethod:
	@classmethod
	def indexbased(cls, i, colors = COLORS):
		"""Simply return the i-th color."""
		return colors[i]

	@classmethod
	def twotone(cls, i, colors = COLORS):
		"""Return the 0-th color if i is even and 1st if i is oddd"""
		return colors[i%2]

	@classmethod
	def change_every(cls, x, i, colors = COLORS):
		"""Change the color every x digits"""
		return colors[i//x]

class ScriptRenderer:
	def __init__(self, dimensions, constant, digitrange, outputfp, **kwargs):
		self.dimensions = dimensions
		self.constant = constant
		self.digitrange = digitrange
		self.outputfp = outputfp

		self.img = Image.new('RGB', (dimensions), color = 'black')
		self.x, self.y = self.img.width // 2, self.img.height // 2
		self.board = ImageDraw.Draw(self.img) # The drawing board

	def run(self):
		for index in range(self.digitrange):
			digit = int(self.constant[index])
			self.loop_iteration(index, digit)
		self.save(self.outputfp)

	def draw_line(self, angle, fill, width, **kwargs):
		"""Draw a line at `angle` degrees from the center."""
		a, b = get_coords_for_line(self.x, self.y, angle, 0, 0)
		coords = ((self.x, self.y), (a, b))

		self.board.line(coords, fill = fill, width = width, **kwargs)

	def loop_iteration(self, index, digit):
		"""Called for each digit in the constant, the arguments provided are the
		digit and the index of said digiit
		"""
		raise NotImplementedError("This should be implemented in derived classes.")

	def save(self, fp, resize = False, resize_dimensions = None):
		img = self.img
		if resize:
			img = img.resize(resize_dimensions, resample = Image.BOX)
		img.save(fp)

class DigitPlusIndexRadians(ScriptRenderer):
	"""
	Draw a line at (digit + index of digit) radians.
	A color method `coloring_method` can be provided, this method
	should only take one integer argument between 0 and 9.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.coloring_method = kwargs.get('coloring_method', ColorMethod.indexbased)

	def loop_iteration(self, index, digit):
		angle = math.degrees(index + digit)
		color = self.coloring_method(digit)

		self.draw_line(angle, color, 5)

class DigitPlusZeroPointIndexRadians(ScriptRenderer):
	"""
	Draw a line at (digit + 0.index_of_digit) radians.
	Each line is given the digit-th element of the COLORS constant.
	"""
	def loop_iteration(self, index, digit):
		angle = math.degrees(digit + float(f'0.{index}'))
		color = ColorMethod.indexbased(digit)

		self.draw_line(angle, color, 5)

class AverageOfDigitsRadians(ScriptRenderer):
	"""
	Calculate a running average x of the first `digitrange` digits of pi and
	Draw a line at x radians as x approaches the true average of the digits of pi.
	Change the color of the lines after every `s` lines.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.sum_value = 0

	def loop_iteration(self, index, digit):
		self.sum_value += digit
		angle = math.degrees(self.sum_value / (index+1))
		color = ColorMethod.change_every(1000, index)

		self.draw_line(angle, color, 3)

### Actually run the stuff here
def main():
	# DigitPlusIndexRadians((4096, 4096), PI, 10000, 'output.png').run()
	# DigitPlusZeroPointIndexRadians((4096, 4096), PI, 10000, 'output.png').run()
	AverageOfDigitsRadians((4096, 4096), PI, 10000, 'output.png').run()

def run_all(dimensions, constant, digitrange):
	arguments = {'dimensions' : dimensions,
				'constant' : constant,
				'digitrange' : digitrange}

	scripts = [
	DigitPlusIndexRadians(**arguments, coloring_method = ColorMethod.indexbased, outputfp = 'digit_plus_index_chaos.png'),
	DigitPlusIndexRadians(**arguments, coloring_method = ColorMethod.twotone, outputfp = 'digit_plus_index_twotone.png'),
	DigitPlusZeroPointIndexRadians(**arguments, outputfp = 'digit_plus_zero_point_index.png'),
	AverageOfDigitsRadians(**arguments, outputfp = 'average_of_index.png')
	]

	for script in scripts:
		print(f'Rendering {script.__class__.__name__}...')
		script.run()

if __name__ == '__main__':
	run_all((4096, 4096), PI, 10000)