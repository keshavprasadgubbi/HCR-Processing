# *** Author: Keshava Prasad Gubbi***
# Script for pre-processing Inbal's HCR Lines.
# DONE: Read the filenames and split and determine names of sig1, sig2 and ref channels
# DONE: Split the Czi imagefilename into respective channels and save it as nrrd with respective names as per channels.

import os
import numpy as np
import re
import nrrd
from aicsimageio import AICSImage
import SimpleITK as sitk
from numpy import ndarray

file_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data\20210302_rspo1_cckb'
ref_num = 0  # the reference channel has been always set to 0 after consultation with Inbal.


def create_channel_folder(path):
    if not os.path.exists(path):
        print(f'Creating {path}')
        os.makedirs(path, exist_ok=True)
        return path


def split_names(f):
    e_name, signal_ch1_name, signal_ch2_name, reference_ch_name = re.split(r'_ch\d_', f)
    d, ext = reference_ch_name.split('.', 1)
    ref_ch_name, fish_number = d.split('_', 1)
    e1_name, f = e_name.rsplit('_', 1)
    days, e_name = e1_name.split('_', 1)
    print('fish_num:', fish_number)
    print('ref_ch_name:', ref_ch_name)
    print('sig_ch1_name:', signal_ch1_name)
    print('sig_ch2_name:', signal_ch2_name)
    print('embryo_name:', embryo_name)
    return fish_number, reference_ch_name, signal_ch1_name, signal_ch2_name, e_name


def get_image_data(f):
    num_stacks, h, w = f.shape[3:]
    # Determine voxel spacing - x, y for use later while writing nrrd files to be of correct pixel spacing. This info
    # can be verified by in Fiji by [ image -> Properties]
    voxel_x, voxel_y, voxel_z = f.get_physical_pixel_size()[:3]  # read_voxel_size(first_channel_data)
    if voxel_z != 1e-6:
        print("Unwanted Voxel depth Value. Will be reset to : 1e-6.")
    return num_stacks, h, w, voxel_x, voxel_y, voxel_z


# def image_to_nrrd(image, channel_name, channel_num):
#     writer = sitk.ImageFileWriter()
#     outputImageFileName = f"{embryo_name}_{fish_num}_{channel_num}_{channel_name}"
#     writer.SetFileName(outputImageFileName)
#     Header = {'units': ['m', 'm', 'm'], 'spacings': [voxel_width, voxel_height, 1e-6]}
#     writer.Execute(os.path.join(preprocessed_path, "outputImageFileName.nrrd"), image, header=Header)
#     return


########Splitting Channels####################
for file in os.listdir(file_path):
    if file.endswith('.czi'):
        print('Working with Image: ', file)

        # Split the file name to obtain respective channel names and fish number for a given HCR line.
        fish_num, reference_ch_name, sig_ch1_name, sig_ch2_name, embryo_name = split_names(file)

        # Creating folders for respective embryo/HCR line being analyzed
        preprocessed_path = file_path + f'/preprocessed/{embryo_name}_{fish_num}/'
        create_channel_folder(preprocessed_path)

        # Read the CZI Image. "c" will be the image object henceforth
        c = AICSImage(os.path.join(file_path, file))
        N_stacks, height, width, voxel_width, voxel_height, voxel_depth = get_image_data(c)
        print("Height, Width of image stack:", height, ",", width, f"with {N_stacks} stacks!")
        print("Voxel Details (x, y, depth):", voxel_width, ",", voxel_height, ",", voxel_depth)

        # Obtain the image data from respective channels
        # B=0 is default value. Ignore User Warnings!
        first_channel_data: ndarray = c.get_image_data("ZYX", B=0, C=0, S=0, T=0)
        second_channel_data: ndarray = c.get_image_data("ZYX", B=0, C=1, S=0, T=0)
        third_channel_data: ndarray = c.get_image_data("ZYX", B=0, C=2, S=0, T=0)

        # Stack the 3D np array to form an image stack, for each channel
        RImage: ndarray = np.stack(first_channel_data).astype('uint8')
        S1Image: ndarray = np.stack(second_channel_data).astype('uint8')
        S2Image: ndarray = np.stack(third_channel_data).astype('uint8')


        def image_to_nrrd(image, channel_name, channel_num):
            Header = {'units': ['m', 'm', 'm'], 'spacings': [voxel_width, voxel_height, 1e-6]}
            image_name = f'{embryo_name}_{fish_num}_{channel_num}_{channel_name}'
            print(f'Creating nrrd image with name : {image_name}.nrrd')
            nrrd_image = nrrd.write(os.path.join(preprocessed_path, f"{image_name}.nrrd"), image, index_order='C',
                                    header=Header)
            return nrrd_image


        # # ### Writing the individual Channels into nrrd format
        print('Writing the individual Channels into nrrd format!')
        



        # nrrd.write(os.path.join(processed_path, f"{embryo_name}_{fish_num}_ch0_{reference_ch_name}.nrrd"), RImage,
        #            index_order='C', header={'units': ['m', 'm', 'm'], 'spacings': [voxel_width, voxel_height, 1e-6]})
        # print(f'Creating nrrd file for Signal1 Channel with name : {embryo_name}_{fish_num}_ch1_{sig_ch1_name}.nrrd')
        # nrrd.write(os.path.join(processed_path, f"{embryo_name}_{fish_num}_ch1_{sig_ch1_name}.nrrd"), S1Image,
        #            index_order='C')
        # print(f'Creating nrrd file Signal2 Channel with name : {embryo_name}_{fish_num}_ch2_{sig_ch2_name}.nrrd')
        # nrrd.write(os.path.join(processed_path, f"{embryo_name}_{fish_num}_ch2_{sig_ch2_name}.nrrd"), S2Image,
        #            index_order='C')

        print(f'###################### Completed processing {file} ###################### ')
