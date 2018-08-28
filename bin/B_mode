#!/usr/bin/env python3
#
# Copyright (C) 2018 William Meng
#
# This file is part of rtl_ultrasound
#
# rtl_ultrasound is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rtl_ultrasound is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rtl_ultrasound.  If not, see <http://www.gnu.org/licenses/>.

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample
import cv2

default_params = {
    'sample_rate': 2.4e6,
    'upsampling_factor': 10,
    'trigger_ratio': 0.4,
    'trigger_holdoff_us': 220,
    'max_depth_cm': 10,
    'angle_range': np.pi/2,

}

def generate_image(samples, params=default_params, verbose=False):
    sample_rate = params['sample_rate']
    upsampling_factor = params['upsampling_factor']
    resampled = resample(samples, len(samples) * upsampling_factor)
    fs = sample_rate * upsampling_factor
    Ts = 1e6/fs # time per sample after resampling, in microseconds
    envelope = np.multiply(np.abs(resampled), 2**16).astype('uint16')
    if verbose:
        print("Resampled at:")
        print("fs = %.2f Msps" % (fs/1e6))
        print("Ts = {} microseconds".format(Ts))
        print("Type of resampled data: {}".format(type(resampled[0])))
        print("Type of envelope data: {}".format(type(envelope[0])))
        print("First element of envelope: {}".format(envelope[0]))

    max_envelope = np.max(envelope)
    trigger_level = int(params['trigger_ratio'] * max_envelope)
    trigger_holdoff_us = params['trigger_holdoff_us'] # trigger holdoff time in microseconds
    trigger_holdoff = int(trigger_holdoff_us / Ts) # trigger holdoff in # of samples
    if verbose:
        print("max(envelope) = {}".format(max_envelope))
        print("Trigger level = {}".format(trigger_level))
        print("Trigger holdoff = {} microseconds = {} samples".format(trigger_holdoff_us, trigger_holdoff))

    prev_trigger = -trigger_holdoff # allow first trigger to be at 0th sample
    slice_indices = list()
    env_list = envelope.tolist()
    if verbose:
        print("env_list data type: {}".format(type(env_list[0])))

    for i in range(len(env_list)):
        if i >= prev_trigger + trigger_holdoff:
            if env_list[i] > trigger_level:
                slice_indices.append(i)
                prev_trigger = i

    if verbose:
        print("Triggered {} times".format(len(slice_indices)))

    # slice array and vstack
    diffs = np.diff(slice_indices)
    min_diff = np.min(diffs)
    if verbose:
        print("Choosing the minimum diff, {}, as the length of each scan line".format(min_diff))

    scan_lines = list()
    for index in slice_indices:
        if len(envelope) < index + min_diff: # not enough samples left for a complete scanline
            break

        scan_line = envelope[index:index+min_diff]
        scan_lines.append(scan_line)

    if verbose:
        print("Created {} scan lines".format(len(scan_lines)))

    image = np.vstack(tuple(scan_lines))
    if verbose:
        print("Type of image pixels: {}".format(type(image[0, 0])))
        print("Image dimensions: {}".format(image.shape))

    max_depth_cm = params['max_depth_cm'] # maximum round trip distance for ultrasound wave to travel
    v = 1498 # speed of sound in water (meters per second)
    v_cm_us = v*100/1e6 # speed of sound in water (cm per microsecond)
    max_depth_time = max_depth_cm / v_cm_us # how many microseconds to keep in each scan line
    max_depth_samples = int(max_depth_time / Ts) # how many samples to keep in each scan line
    if verbose:
        print("Max depth = {} cm = {} µs = {} samples".format(max_depth_cm, max_depth_time, max_depth_samples))

    im_in = image[:, :max_depth_samples] # cut off any data beyond max depth

    maxRadius = im_in.shape[1]

    angle_range = params['angle_range'] # range of angle swept by transducer (radians)
    theta_scale_factor = im_in.shape[0] / angle_range # rows per radian
    theta_min = 3/2*np.pi - angle_range/2
    theta_max = 3/2*np.pi + angle_range/2
    if verbose:
        print("maxRadius = {} pixels".format(maxRadius))
        print("{} rows per radian".format(theta_scale_factor))
        print("theta: [{}, {}] radians".format(theta_min, theta_max))

    # pad the image
    pad_below = int(theta_min * theta_scale_factor) # how many rows to pad below theta_min
    pad_above = int((2*np.pi - theta_max) * theta_scale_factor) # how mahy rows to pad above theta_max
    if verbose:
        print("Padding {} above and {} below".format(pad_above, pad_below))

    im_below = np.zeros((pad_below, maxRadius), dtype='uint16')
    im_above = np.zeros((pad_above, maxRadius), dtype='uint16')

    padded_image = np.vstack((im_above, im_in, im_below))
    # scale image
    scaled_image = cv2.resize(padded_image, (2*maxRadius, maxRadius), interpolation=cv2.INTER_CUBIC)

    # transform image
    center = (int(scaled_image.shape[1]/2), 0) # (x, y) coordinate from top-left of image
    flags = cv2.WARP_INVERSE_MAP
    im_out = cv2.linearPolar(scaled_image, center, maxRadius, flags)

    return im_out


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate B-mode ultrasound image from a npz file containing ultrasound data')
    parser.add_argument('-v', '--verbose', action='store_true', help="enable verbose output")
    parser.add_argument('--data', metavar='<data filename>', dest='filename', type=str,
                        required=True, help="Filename of .npz data file")
    args = parser.parse_args()

    try:
        assert(args.filename.endswith('.npz'))
    except AssertionError:
        print("ERROR: Provided data file must have .npz file extension.")
        sys.exit()

    try:
        data = np.load(args.filename)
        samples = data['samples']
        sample_rate = int(data['sample_rate'])
    except:
        print("ERROR: Failed to load data. Incorrect format.")
        sys.exit()


    params = default_params
    params['sample_rate'] = sample_rate
    im_out = generate_image(samples, params=params, verbose=args.verbose)

    plt.imshow(im_out, cmap='gray')
    title_text = "image generated from {}".format(args.filename)
    title_text += "\nsample_rate = {} Msps".format(params['sample_rate'] / 1e6)
    title_text += "  upsampling {}x".format(params['upsampling_factor'])
    title_text += "\ntrigger ratio = {}".format(params['trigger_ratio'])
    title_text += "  trigger holdoff = {} µs".format(params['trigger_holdoff_us'])
    title_text += "\nmax depth = {} cm".format(params['max_depth_cm'])
    title_text += "  angle range = {}º".format(params['angle_range'] * 180 / np.pi)
    plt.title(title_text)
    destfile = args.filename.rstrip('npz') + 'png'
    plt.savefig(destfile, dpi=300)
    plt.show()

if __name__ == '__main__':
    main()

