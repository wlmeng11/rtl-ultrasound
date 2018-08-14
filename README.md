# rtlsdr_ultrasound

TODO: get badges
* Travis
* coverage
* PyPI (badge.fury.io)
* license
* gitter

pic of setup & ultrasound image

## Installation
`pip3 install rtlsdr_ultrasound`

### Manual installation
Install the system dependencies:
* Python 3
* librtlsdr

Clone the development repo:  
`git clone git@github.com:wlmeng11/rtlsdr_ultrasound.git`

Install the python package dependencies:  
`pip3 install -r requirements.txt`


## Usage
This software was designed to be used with [RTL-SDR v3](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/)
in conjunction with the [SimpleRick](https://github.com/wlmeng11/SimpleRick) hardware.

However, this software can be also used with any ultrasound hardware that
provides an analog signal output that can be fed to the input of the RTL-SDR.

## How it works
A fairly comprehensive overview of the entire process from data acquisition to rendered image
can be found [here](experiments/20180813/rtlsdr_ultrasound_test.ipynb).

Essentially, it boils down to these steps:
* blah

## License
The software contained herein is distributed according to the terms of the GNU General Public License version 3.

### Credit
* [pyrtlsdr](https://github.com/roger-/pyrtlsdr) is Copyright (C) 2013 by Roger https://github.com/roger-
* [un0rick](https://github.com/kelu124/un0rick) is Copyright Kelu124 (kelu124@gmail.com) 2018

### Copyright
Copyright (C) 2018 William Meng
