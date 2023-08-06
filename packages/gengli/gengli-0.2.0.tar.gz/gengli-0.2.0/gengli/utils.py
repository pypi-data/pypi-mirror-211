"""
gengli.utils
============

	Gatherss some utilities required by the glicth generator, implementing functions to measure the distance (discrepancy) between glitches and resampling them.
"""
import itertools
from scipy.stats import wasserstein_distance
import scipy.signal
import numpy as np
import ray

#############################################################################################################
#############################################################################################################

@ray.remote
def metrics(fake1, fake2):
	"""
	Computes the similarity betweek glitch fake1 and fake2. It uses ray to parellelize and speed up the computations. It assumes that `ray.init()` has been already called.
	The similarity is computed using three different metrics:
	
	- Wasserstein distance
	- Mismatch (as standard in GW data analysis)
	- Mis-correlation (1-normalized correlation)
	
	All the three are returned.
	
	Parameters
	----------
	
	fake1: :class:`~numpy:numpy.ndarray`
		First GAN-generated glitch (sampled at 4096 Hz)
	fake2: :class:`~numpy:numpy.ndarray`
		Second GAN-generated glitch (sampled at 4096 Hz)
	
	Returns
	-------
	wass_value: float
		Wasserstein distance between the two glitches
	match_value: float
		Match between the two glitches
	ccor_value: float
		Correlation between the two glitches
		
	"""
	# To avoid dtype problems
	fake1 = np.asarray(fake1, dtype=np.float64) #asarray, avoids copies, when necessary
	fake2 = np.asarray(fake2, dtype=np.float64)

	# Correlation
	ccov = np.correlate(fake1 - fake1.mean(),
						fake2 - fake2.mean(),
						mode='full') #Maybe dropping mode full and keeping valid might help in speeding up??
	ccor = ccov / (len(fake1) * fake1.std() * fake2.std())
	ccor_value = max(np.abs(ccor))

	# PyCBC match
	data_points = len(fake1)
	samp_freq = 4096

	#F1 = pycbc_TimeSeries(fake1, delta_t=data_points/samp_freq, epoch=0)
	#F2 = pycbc_TimeSeries(fake2, delta_t=data_points/samp_freq, epoch=0)

	fd_fake1, fd_fake2 = np.fft.rfft(fake1), np.fft.rfft(fake2)
	corr_fd = fd_fake1*fd_fake2/np.sqrt(np.vdot(fd_fake1,fd_fake1)*np.vdot(fd_fake2,fd_fake2))

	match_value = np.max(np.abs(np.fft.irfft(corr_fd)))*len(corr_fd)

	# Wasserstein distance

	wass_value = wasserstein_distance(fake1, fake2)
	return wass_value, 1-match_value, 1-ccor_value

@ray.remote
def ray_dummy():
	return np.nan, np.nan, np.nan
	

def compute_distance_matrix(set1, set2):
	"""
	It computes the distance matrix between each pairs of two sets of glitches. The metric consists in 3 different quantities:
	
	- Wasserstein distance
	- Match (as standard in GW data analysis)
	- Correlation

	If the input are two sets of N and M glitches, the distance matrix will be a `(N,M,3)` matrix, where the the ij elements holds the 3 dimensional distances between the i-th element of the first set and the j-th element of the second set.
	

	Parameters
	----------
	
	set1: :class:`~numpy:numpy.ndarray`
		First set of glitches (shape `(N,D)`)
	
	set2: :class:`~numpy:numpy.ndarray`
		Second set of glitches (shape `(M,D)`)
	
	Returns
	-------
	
	distance_matrix: :class:`~numpy:numpy.ndarray`
		Distance matrix with shape `(N,M,3)`
	"""
	assert isinstance(set1, np.ndarray) and  isinstance(set2, np.ndarray), "Glitch sets must be arrays"
	set1, set2 = np.atleast_2d(set1), np.atleast_2d(set2)
	assert set1.ndim == set2.ndim == 2, "Glitch sets must be two dimensional"
	assert set1.shape[1] == set2.shape[1], "Glitch sets must be evaluated on the a grid of the same size. {} and {} given".format(set1.shape[1], set2.shape[1])
	
	same_set = np.allclose(set1, set2) if (set1.shape == set2.shape) else False 
	
	if same_set:
		distance_matrix = [metrics.remote(s1,s2) if i>=j else ray_dummy.remote() for (i,s1), (j,s2) in itertools.product(enumerate(set1), enumerate(set2)) ]
	else:
		distance_matrix = [metrics.remote(s1,s2) for s1, s2 in itertools.product(set1, set2)]
	distance_matrix = np.array(ray.get(distance_matrix)).reshape((set1.shape[0], set2.shape[0], 3))

	if same_set:
		ids_ = np.triu_indices(distance_matrix.shape[0])
		for i,j in zip(*ids_): distance_matrix[i,j,:] = distance_matrix[j,i,:]
	
	return distance_matrix

#############################################################################################################
#############################################################################################################
def rescale_glitch(glitch, snr, srate):
	"""
	Rescale the glitch to the user given signal-to-noise ratio.
	
	Parameters
	----------
	
	glitch: :class:`~numpy:numpy.ndarray`
		An array holding one or several glitches
	
	snr: float, :class:`~numpy:numpy.ndarray`
		Signal-to-noise (snr) ratio of the returned glitches. The snr is computed *according to the lalsuite white noise normalization*.
		If None, no rescaling will be performed
					
	srate: float
		Sampling rate for the given glitch (to compute the proper white noise normalization)

	Returns
	-------
		rescaled_glitch: :class:`~numpy:numpy.ndarray`
			The rescaled glitch(es)
	"""
	glitch = np.asarray(glitch)
	if snr is not None:
			#Computing the actual SNR
		df = srate/glitch.shape[-1]
			#this is done in TD (almost correct)
			#true_snr = np.sqrt(4.*df*np.sum(np.square(glitch)/srate**2, axis =-1))

			#This agrees with pycbc (!)
			#sigma_sq is <g|g>, which is the square of the SNR
		glitch_FD = np.fft.rfft(glitch, axis = -1)/srate
		true_sigma_sq = 4.0 * df*np.sum(np.multiply(np.conj(glitch_FD), glitch_FD), axis =-1).real #equivalent to vdot
			
		glitch = (glitch.T * snr/np.sqrt(true_sigma_sq)).T
	return glitch


def low_pass_glitch(glitch, fhigh, srate):
	"""
	Low pass filter the glitch according to the user given high-frequency cut-off.
	
	Parameters
	----------
	
	glitch: :class:`~numpy:numpy.ndarray`
		An array holding one or several glitches

	fhigh: float
		High frequency cutoff for the low pass filter. If `None`, no filtering will be performed
		Usually, a blip glitch has a high frequency cutoff of `250 Hz`.

	srate: float
		Sampling rate of the given glitch

	Returns
	-------
		filtered_glitch: :class:`~numpy:numpy.ndarray`
			The lowpass filtered glitch(es)
	"""
	glitch = np.asarray(glitch)
	if isinstance(fhigh, (float,int)):
		order = 3 #order of the filter (is it a good default?)
		normal_cutoff = fhigh/(0.5*srate) #fhigh/nyquist
		b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
		glitch = scipy.signal.filtfilt(b, a, glitch, axis = -1)
	return glitch

def resample_glitch(glitch, srate, new_srate):
	"""
	Convenience wrap to :func:`~scipy:scipy.signal.resample` to change the sampling rate of a glitch
	
	Parameters
	----------
	glitch: :class:`~numpy:numpy.ndarray`
		An array holding one or several glitches
		
	srate: float
		Sampling rate of the given glitch
			
	new_srate: float
		Sampling rate at which the new glitch should be evaluated
		
	Returns
	-------
	resampled_glitch: :class:`~numpy:numpy.ndarray`
		New resampled glitch
		
	"""
	#FIXME: should you move this into glitch_generator?
	glitch = np.asarray(glitch)
	old_length = glitch.shape[-1]  #(N,D)
	new_length = int(old_length*new_srate/srate)
		# we resample to desired sampling rate with scipy
	resampled_glitch = scipy.signal.resample(glitch, new_length, axis = -1)  # (938, 1) --> (new_length, 1)
		
	return resampled_glitch



