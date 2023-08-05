'''
rampedpyrox was created as a thesis dissertation supplement by:

	Jordon D. Hemingway, MIT/WHOI Joint Program
	Currently Assistant Professor, ETH Zurich
	jordon.hemingway@erdw.ethz.ch

source code can be found at:
	
	https://github.com/FluvialSeds/rampedpyrox

documentation can be found at:

	http://rampedpyrox.readthedocs.io

Version 1.0.4 is current as of 29 May 2023 and reflects the notation used
in Hemingway et al. Biogeosciences, 2017.

To do for future versions:
* Change exception structure to "try/except"
* Add more robust nose testing suite for debugging

REVISION NOTES:
---------------

2023.05.29: CHANGED TO 'display.precison' FOR PANDAS V 2.0
2023.05.29: CHANGED 'parse_dates = True' TO PARSE AS OBJECT AND THEN
			PARSE DIRECTLY USING 'to_datetime()'. FIXED WARNING.
'''

from __future__ import(
	division,
	print_function,
	)

__version__ = '1.0.4'

__docformat__ = 'restructuredtext en'


#import timedata classes
from .timedata import(
	RpoThermogram,
	BioDecay,
	)

#import model classes
from .model import(
	Daem,
	LaplaceTransform,
	)

#import ratedata classes
from .ratedata import(
	EnergyComplex,
	kDistribution,
	)

#import results classes
from .results import(
	RpoIsotopes,
	)

#import package-level functions
from .core_functions import(
	assert_len,
	calc_L_curve,
	derivatize,
	extract_moments,
	plot_tg_isotopes,
	)
