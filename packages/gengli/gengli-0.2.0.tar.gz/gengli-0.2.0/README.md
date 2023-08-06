# gengli

`gengli` (generating glitches) is a package to provide an handy an easy to use interface to CTGAN, a generative adversarial neural network to generate glitches. A "glitch" is a non stationary noise transient recorded in Gravitational Waves (GW) interferometer. As it resembles some GW signals, their appearece hinders the searches for such signal, downgrading the instrument sensitivity.
A nice characterization of glitches can enable lots of exciting GW science!

This network is trained with real (although heavily preprocessed) glitch and when given some random noise, it outputs a whithened glitch. `gengli` offers a simple API to access the network, enabling some post-processing of the generated glitch that can be useful for downstream analysis. In more, details it allow the user to:

- Resample the glitch
- Lowpass (i.e. removing spurious high frequency content) and window
- Scale it to achieve a target SNR
- Select among random glitches only those within a given percentile w.r.t. to some anomaly score (more on the paper). This enables the user to get only "normal" glitches and/or "atypical" glitches.

You can read the full documentation [here](https://melissa.lopez.docs.ligo.org/gengli/index.html)!

## How to install

To install the latest released version of gengli, available on PyPI:

```Bash
pip install gengli
```

### From the repo

If you want to install the code from this repo, you can use the `Makefile` provided:

```Bash
git clone https://git.ligo.org/melissa.lopez/gengli.git
cd gengli
make install
```

If you want to build a local version of the documention, just type `make docs`. This will create the folder `docs/__build/` where all the relevant html docs will be located.

### With a conda environment

If you don't want to mess up with your existing conda installations, this will create a fresh new conda environment that only contains `gengli` and its dependencies:

```Bash
conda create --name gengli_env python=3.9
conda activate gengli_env
git clone https://git.ligo.org/melissa.lopez/gengli.git
cd gengli
python setup.py sdist
pip install dist/gengli-0.1.0.tar.gz 
```

A ready made conda environment is also provided in `env.yml`.
To use it just type:

```Bash
conda env create --file env.yml
```

This will create an environment with all the dependencies (and `gengli` installed)

## How to generate a glitch

To generate a glitch, you will need to instantiate a `glitch_generator` object:

```Python
import gengli
g = gengli.glitch_generator('L1')
```

You should provide the generator the weights of the generator network. Some default (and reviewed) weights are relaesed with this package: if you want to use them, you should just pass the string `L1` or `H1` to specify which interferometer you want to consider and the weights will be loaded authomatically.

To generate the raw glitch (as output by the network):
```Python
g_raw = g.get_glitch()
```

The glitch is whithened and evaluted on a default time grid sampled at 4096Hz. It has a characteristic shape:

![raw_glitch](docs/img/raw_glitch.png)


The function `get_glitch` also provides an easy to use API to the post-processing operations described above. For instance, to generate 10 glitches, filtered and windowed with an SNR of 15 and evaluated at a lower sampling rate, you can just type:

```Python
g_processed = g.get_glitch(10,
	srate = 2048,
	snr = 15,
	alpha = 0.2,
	fhigh = 250)
```

The generated glitches will look quite different from before:

![processed_glitch](docs/img/glitch.png)

If you want to get three anomalous glitches, you can play with the `percentiles` parameter of `get_glitch_confidence_interval`. For instance:

```Python
g.get_glitch_confidence_interval(percentiles = (0,80),
	n_glitches = 3,
	snr = 20)
```

This will take a while to run as it will call internally (only once) `glitch_generator.initialize_benchmark_set`, which creates a set of benchmark glitches to compute the "anomaly score" against.
To have more controls of the parameters of `initialize_benchmark_set`, you can call it from your script: you will note that, once such initialization is done, `get_glitch` will run much faster!

You can take a look at some [examples](examples) in a dedicated folder.

For more information, you can read the [docs](https://gengli.readthedocs.io/en/latest/).


## About

This project is developed in the GW group at Utrecht Univerisity. Many people were involved in this project:

- Vincent Boudart
- Kerwin Buijsman
- Sarah Caudill
- Melissa Lopez (corresponding author: [m.lopez@uu.nl](mailto:m.lopez@uu.nl))
- Amit Reza
- Stefano Schmidt (package maintener: [s.schmidt@uu.nl](mailto:s.schmidt@uu.nl))

If you want to have more information, or just to say hello, please feel free to contact any of us!

## Publications

If you find our work useful, please consider reading and citing our publications.

The main work, detailing the method and its performances, is the following:

```
@article{Lopez:2022lkd,
    author = "Lopez, Melissa and Boudart, Vincent and Buijsman, Kerwin and Reza, Amit and Caudill, Sarah",
    title = "{Simulating transient noise bursts in LIGO with generative adversarial networks}",
    eprint = "2203.06494",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.IM",
    doi = "10.1103/PhysRevD.106.023027",
    journal = "Phys. Rev. D",
    volume = "106",
    number = "2",
    pages = "023027",
    year = "2022"
}
```

A follow up paper describes `gengli` and its features, providing more details on the network architecture and training:

```
@article{Lopez:2022dho,
    author = "Lopez, Melissa and Boudart, Vincent and Schmidt, Stefano and Caudill, Sarah",
    title = "{Simulating Transient Noise Bursts in LIGO with gengli}",
    eprint = "2205.09204",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.IM",
    month = "5",
    year = "2022"
}
```

