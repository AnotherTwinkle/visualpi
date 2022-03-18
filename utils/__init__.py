from .PIVALUE import PI
def create_coord_data(x, y):
	a = []
	for yp in range(0, y):
		a.extend([(xp, yp) for xp in range(0, x)])

	return a