"""
gengli
======
	A package to generate transient noise bursts (a.k.a. glitches) from LIGO with a Generative Adversarial Neural Networks. `gengli` can also process the generated glitches according to the user's needs, to make them ready for injection in real noise.
	
	The full repository is available at `git.ligo.org/melissa.lopez/gengli <https://git.ligo.org/melissa.lopez/gengli>`_

"""
from .glitch_generator import glitch_generator
