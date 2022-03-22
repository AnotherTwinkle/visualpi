from .PIVALUE import PI
from .EVALUE import E
from .PHIVALUE import PHI

def create_coord_data(x, y):
	a = []
	for yp in range(0, y):
		a.extend([(xp, yp) for xp in range(0, x)])

	return a