# *** Author: Keshava Prasad Gubbi***
# Script for pre-processing Inbal's HCR Lines.
# DONE: Read the filenames and split and determine names of sig1, sig2 and ref channels
# DONE: Split the Czi imagefilename into respective channels and save it as nrrd with respective names as per channels.

import os
import numpy as np
# from aicspylibczi import CziFile
import re
import nrrd
from aicsimageio import AICSImage
import SimpleITK as sitk
# from skimage import io


file_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data\20210302_rspo1_cckb'
# preprocessed_path = file_path + '/preprocessed/'
# ref_num = int(input('Enter Reference Channel Number: (please enter 0 if refrence channel in image is channel1!)'))
ref_num = 0


def create_channel_folder(path):
    if not os.path.exists(path):
        print(f'Creating {path}')
        os.makedirs(path, exist_ok=True)
        return path


def split_names(file):
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
    return fish_num, ref_ch_name, sig_ch1_name, sig_ch2_name, embryo_name


def read_voxel_size(f):
    '''
    The idea is to get the respective ndarray and convert it into a image and tehn obtain its voxel spacing
    and the use these values'''
    print("********Reading Voxel Size********")
    im = sitk.GetImageFromArray(f)
    print(im.GetSize())
    print(type(im))
    width, height, depth = im.GetSpacing()
    print('Current voxel spacing:', width, height)
    return width, height


########Splitting Channels####################
for file in os.listdir(file_path):
    if file.endswith('.czi'):
        print('Image name: ', file)

        fish_num, ref_ch_name, sig_ch1_name, sig_ch2_name, embryo_name = split_names(file)

        # Read the CZI Image. "c" will be the image object henceforth
        c = AICSImage(os.path.join(file_path, file))
        *a, ch, dep, h, w = c.shape
        print("Height, Width of image stack:", h, ",", w)

        # Obtain the image data from respective channels
        first_channel_data = c.get_image_data("ZYX", C=0, S=0, T=0)
        second_channel_data = c.get_image_data("ZYX", C=1, S=0, T=0)
        third_channel_data = c.get_image_data("ZYX", C=2, S=0, T=0)

        # print(first_channel_data.shape)
        RImage = np.stack(first_channel_data).astype('uint8')
        S1Image = np.stack(second_channel_data).astype('uint8')
        S2Image = np.stack(third_channel_data).astype('uint8')

        # Determine voxel spacing - x, y for use later while writing nrrd files
        voxel_width, voxel_height = read_voxel_size(RImage)
        # print(voxel_width, voxel_height)

        preprocessed_path = file_path + f'/preprocessed/{embryo_name}_{fish_num}/'
        create_channel_folder(preprocessed_path)

        # ### Writing the individual Channels into nrrd format
        # print('Writing the individual Channels into nrrd format!')
        #
        # print(f'Creating Reference Channel nrrd file with name : {embryo_name}_{fish_num}_ch0_{ref_ch_name}.nrrd ')
        # nrrd.write(os.path.join(preprocessed_path, f"{embryo_name}_{fish_num}_ch0_{ref_ch_name}.nrrd"), RImage,
        #            index_order='C')
        # print(f'Creating nrrd file for Signal1 Channel with name : {embryo_name}_{fish_num}_ch1_{sig_ch1_name}.nrrd')
        # nrrd.write(os.path.join(preprocessed_path, f"{embryo_name}_{fish_num}_ch1_{sig_ch1_name}.nrrd"), S1Image,
        #            index_order='C')
        # print(f'Creating nrrd file Signal2 Channel with name : {embryo_name}_{fish_num}_ch2_{sig_ch2_name}.nrrd')
        # nrrd.write(os.path.join(preprocessed_path, f"{embryo_name}_{fish_num}_ch2_{sig_ch2_name}.nrrd"), S2Image,
        #            index_order='C')

        print(f'###################### Completed processing {file} ###################### ')