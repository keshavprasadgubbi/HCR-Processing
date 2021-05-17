# *** Author: Keshava Prasad Gubbi***
# Script for pre-processing Inbal's HCR Lines.
# DONE: Read the filenames and split and determine names of sig1, sig2 and ref channels
# DONE: Split the Czi imagefilename into respective channels and save it as nrrd with respective names as per channels.

import os
import numpy as np
from aicspylibczi import CziFile
import re
import nrrd
########Splitting Channels####################

file_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data\20201204_pmch_pmch1'
ref_channel_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data\20201204_pmch_pmch1\reference'
sig_channel_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data\20201204_pmch_pmch1\signal'
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


def create_channel_folder(path):
    if not os.path.exists(path):
        print(f'Creating {path}')
        os.makedirs(path, exist_ok=True)
        return path


def split_czi_channels(czifile):
    czi = CziFile(czifile)
    max_channels = range(*czi.dims_shape()[0]['C'])
    max_slices = range(*czi.dims_shape()[0]['Z'])
    for ch_num in max_channels:
        image_list = []
        for z_plane in max_slices:
            print('imagefilename:', file, ', ch_num:', ch_num, ', z_plane:', z_plane)
            imgarray, shp = czi.read_image(B=0, S=0, C=ch_num, T=0, Z=z_plane)
            image_list.append(np.squeeze(imgarray))
            return ch_num, image_list


for file in os.listdir(file_path):
    if file.endswith('.czi'):
        print(file)
        ref_name, exp_name, sig2_name, sig1_name, f_num = get_channel_names(file)
        create_channel_folder(ref_channel_path)
        create_channel_folder(sig_channel_path)

        channel_number, i_list = split_czi_channels(os.path.join(file_path, file))

        if ref_ch_num == channel_number:
            ref_channel_image = np.stack(i_list).astype('uint8')
            nrrd.write(os.path.join(ref_channel_path, f"{exp_name}_{f_num}_{ref_name}.nrrd"), ref_channel_image,
                       index_order='C')
        else:
            sig_channel_image = np.stack(i_list).astype('uint8')
            nrrd.write(os.path.join(sig_channel_path, f"{exp_name}_{f_num}_{sig1_name}.nrrd"),
                       sig_channel_image, index_order='C')

    else:
        print("Not a .czi file. Please recheck File format!")
##################################################################################################

