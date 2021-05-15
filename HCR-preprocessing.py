# *** Author: Keshava Prasad Gubbi***
# Script for pre-processing Inbal's HCR Lines.
# TODO: Read the filenames and split and determine names of sig1, sig2 and ref channels
# TODO: Split the Czi imagefilename into respective channels and save it as tif with respective names as per channels.
# TODO: Add Gaussian filtering to Images.
# TODO: contrast enhancement, add a binary flag parameter (if needed or not needed)
# TODO: make images sharper: using minimum 3D filtering.
# TODO: Reduce background.
# TODO: after going through all these processing, save as tif files with proper imagefilename names based on respective channels.
# TODO: Create a separate script for automatic creation of alignment script for respective line.

import os
import tifffile as tiff
import numpy as np
from aicspylibczi import CziFile
import glob
import re

########Splitting Channels####################

c_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data\20201204_pmch_pmch1'
original_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1/data/czidata/original/'

if not os.path.exists(original_path):
    print(f'Creating {original_path}')
    os.makedirs(original_path, exist_ok=True)

ref_ch_num = int(input('Enter Reference Channel Number:'))


def get_channel_names(imagefilename):
    name, ext = imagefilename.split('.')
    if ref_ch_num == 0:
        a, sig_ch1_name, ref_ch_name, fish_num = re.split('_ch\d_', name)
    elif ref_ch_num == 1:
        a, ref_ch_name, sig_ch1_name, fish_num = re.split("_ch\d_", name)
    else:
        ref_ch_name, a, sig_ch1_name, fish_num = re.split("_ch\d_", name)
    embryo_name, sig_ch2_name = a.rsplit('_', 1)

    print('fish_num:', fish_num)
    print('ref_ch_name:', ref_ch_name)
    print('sig_ch1_name:', sig_ch1_name)
    print('sig_ch2_name:', sig_ch2_name)
    print('embryo_name:', embryo_name)

    return ref_ch_name, embryo_name, sig_ch2_name, sig_ch1_name, fish_num


for file in os.listdir(c_path):
    if file.endswith('.czi'):
        print(file)
        ref_name, exp_name, sig2_name, sig1_name, f_num = get_channel_names(file)

        czi = CziFile(os.path.join(c_path, file))
        max_channels = range(*czi.dims_shape()[0]['C'])
        max_slices = range(*czi.dims_shape()[0]['Z'])
        for ch_num in max_channels:
            image_list = []
            for z_plane in max_slices:
                print('imagefilename:', file, ', ch_num:', ch_num, ', z_plane:', z_plane)
                imgarray, shp = czi.read_image(B=0, S=0, C=ch_num, T=0, Z=z_plane)
                image_list.append(np.squeeze(imgarray))

                # split_image = split_czi_channels(imagefilename)
                if ref_ch_num == ch_num:
                    ref_channel_image = np.stack(image_list).astype('uint8')
                else:
                    sig_channel_image = np.stack(image_list).astype('uint8')

##################################################################################################

# with tiff.TiffWriter(os.path.join(original_path, f'{name}_ref.tif')) as tifw:
#     print(f'Adding slice {z_plane} to {name}_ref.tif')
#     tifw.write(np.stack(image_list).astype('uint8'))

# with tiff.TiffWriter(os.path.join(original_path, f'{name}_sig.tif')) as tifw:
#     print(f'Adding slice {z_plane} {name}_sig.tif')
#     tifw.write(np.stack(image_list).astype('uint8'))
