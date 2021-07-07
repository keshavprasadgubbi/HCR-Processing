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

file_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data\20210302_rspo1_cckb'
preprocessed_path = file_path + '/preprocessed/'


def create_channel_folder(path):
    if not os.path.exists(path):
        print(f'Creating {path}')
        os.makedirs(path, exist_ok=True)
        return path
########Splitting Channels####################
# ref_num = int(input('Enter Reference Channel Number: (please enter 0 if refrence channel in image is channel1!)'))
ref_num = 0
for file in os.listdir(file_path):
    if file.endswith('.czi'):
        print('Image name: ', file)
        create_channel_folder(preprocessed_path)

        e_name, sig_ch1_name, sig_ch2_name, ref_ch_name = re.split(r'_ch\d_', file)
        c, ext = ref_ch_name.split('.', 1)
        ref_ch_name, fish_num = c.split('_', 1)
        e1_name, f = e_name.rsplit('_', 1)
        days, embryo_name = e1_name.split('_', 1)

        print('fish_num:', fish_num)
        print('ref_ch_name:', ref_ch_name)
        print('sig_ch1_name:', sig_ch1_name)
        print('sig_ch2_name:', sig_ch2_name)
        print('embryo_name:', embryo_name)

        c = CziFile(os.path.join(file_path, file))
        max_channels = range(*c.dims_shape()[0]['C'])
        max_slices = range(*c.dims_shape()[0]['Z'])

        # for ch_num in max_channels:
        for ch_num in range(len(max_channels)):
            print('Processing ch_num:', ch_num, '...........')
            ref_image_list = sig1_image_list = sig2_image_list = []
            for z_plane in max_slices:
                imgarray, shp = c.read_image(B=0, S=0, C=ch_num, T=0, Z=z_plane)

                if ch_num == 0 and ch_num == ref_num:
                    ref_image_list.append(np.squeeze(imgarray))
                elif ch_num == 1:
                    sig1_image_list.append(np.squeeze(imgarray))
                elif ch_num == 2:
                    sig2_image_list.append(np.squeeze(imgarray))
                else:
                    print('Exceeded Maximum number of channels')

        RImage = np.stack(ref_image_list).astype('uint8')

        S1Image = np.stack(sig1_image_list).astype('uint8')

        S2Image = np.stack(sig1_image_list).astype('uint8')

        ### Writing the individual Channels into nrrd format
        print('Writing the individual Channels into nrrd format!')

        print(f'Creating Reference Channel nrrd file with name : {embryo_name}_{fish_num}_ch0_{ref_ch_name}.nrrd ')
        nrrd.write(os.path.join(file_path, f"{embryo_name}_{fish_num}_ch0_{ref_ch_name}.nrrd"), RImage, index_order='C')
        print(f'Creating nrrd file for Signal1 Channel with name : {embryo_name}_{fish_num}_ch1_{sig_ch1_name}.nrrd')
        nrrd.write(os.path.join(file_path, f"{embryo_name}_{fish_num}_ch1_{sig_ch1_name}.nrrd"), S1Image,
                   index_order='C')
        print(f'Creating nrrd file Signal2 Channel with name : {embryo_name}_{fish_num}_ch2_{sig_ch1_name}.nrrd')
        nrrd.write(os.path.join(file_path, f"{embryo_name}_{fish_num}_ch2_{sig_ch2_name}.nrrd"), S2Image,
                   index_order='C')

        print(f'###################### Completed processing {file} ###################### ')

