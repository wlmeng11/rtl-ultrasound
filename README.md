# rtl_ultrasound
-----
TODO: logo next to title

TODO: get badges

* build passing (Travis)
* build passing (appveyor)
* coverage x% (coveralls.io)
* docs passing (readthedocs.io)
* code quality (codacy)
* PyPI (badge.fury.io)
* license
* gitter.im
* DOI (zenodo)

pic of setup & ultrasound image

## Installation
### System Dependencies
Install the system dependencies:

* Python 3
* librtlsdr

#### Mac OSX
`brew install python3 librtlsdr`

Warning: If you previously installed software that bundles an out-of-date version of librtlsdr,
you may have to remove it, or overwrite the symlinks for librtlsdr: `brew link --overwrite librtlsdr`

### Automatic installation
Install rtl_ultrasound:  
`pip3 install rtl_ultrasound`

### Manual installation
Clone the development repo:  
`git clone git@github.com:wlmeng11/rtl_ultrasound.git`

Install the python package dependencies:  
`pip3 install -r requirements.txt`

Run the install script:  
`python3 setup.py install`

## Usage
This software is designed to be used with the [RTL-SDR v3](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/)
in conjunction with the [SimpleRick](https://github.com/wlmeng11/SimpleRick) hardware.

However, this software can be also used with any ultrasound hardware which
provides an analog signal output that can be fed to the input of the RTL-SDR.

## Documentation
A fairly comprehensive overview of the entire process from data acquisition to rendered image
can be found [here](experiments/20180813/rtl_ultrasound_test.ipynb).

Essentially, it boils down to these steps:

* acquire IQ samples from RTL-SDR
* upsample
* extract envelope
* split signal into scan lines
* stack scan lines into image
* perform polar to cartesian image transformation

TODO: these steps will be parallelized with multithreading in order to
provide a fast image update rate with pipelining

## License
The software contained in this repository makes use of the pyrtlsdr module, and is therefore a derivative work of pyrtlsdr. As such, this work respects the GPL v3 license of pyrtlsdr and is similarly distributed under GPL v3.

The full text of the license can be found in the [COPYING](COPYING) file.

[pyrtlsdr](https://github.com/roger-/pyrtlsdr) is Copyright (C) 2013 by Roger https://github.com/roger-

[rtl_ultrasound](https://github.com/wlmeng11/rtl_ultrasound/) is Copyright (C) 2018 William Meng
