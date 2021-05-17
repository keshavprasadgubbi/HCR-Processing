# *** Author: Keshava Prasad Gubbi***
# Script for postprocessing Inbal's HCR Lines.

# DONE: Read the aligned .nrrd 32 bit image files after downloading from the cluster, with index order C
# DONE: Convert to 8bit image
# DONE: Enhance contrast on the array
# DONE: write the respective array stack into a tiff file stack.
# DONE: Read the tiff image and unstack page by page and do image processing and restack it
# TODO: Gaussian Filtering/Bilateral Filtering in the array stack.
# TODO: sharpen the image via minimum 3D filter/other sharpening tools.
# TODO: Rewrite the respective array stack into a tiff file stack.
#TODO: Loop over the z dim of the image stack and finish the processing and later restack again


import os
import nrrd
from skimage import io, exposure, filters
from skimage.filters.rank import mean_bilateral
from skimage.morphology import disk
import numpy as np
import tifffile as tiff
file_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data'


def convert_to_8bit(f):
    print("********Checking Image Type********")
    # img = io.imread(f)
    dtype = f.dtype
    print('Old data type:',dtype)
    if dtype != 'uint8':
        f.astype('uint8', copy=False)
        print('New data type:',dtype)
    return f.astype('uint8')


def ce(f):
    # i = img_as_float(io.imread(f)).astype(np.float64)
    logarithmic_corrected = exposure.adjust_log(f, 1)
    return logarithmic_corrected


def tiff_unstackAndrestack(f):
    '''
    :param f: tiff file
    :return: rotated_image_stack
    #1. Iterate through each file as a tiff file.
    #2. split into individual pages //Unstacking
    #3. rotate each page and save the rotated_page into a new list
    #4. restack each array from the list
    '''
    with tiff.TiffFile(f, mode='r+b') as tif:
        print(f' Processing {tif} for rotation...')
        for page in tif.pages:
            #pass
            processed_page = ce(page)
            bilat_img = mean_bilateral(processed_page, disk(20), s0=10, s1=10)
            processed_page_list = []
            processed_page_list.append(bilat_img)
            processed_image_stack = np.stack(processed_image_stack)
    return processed_image_stack.astype('uint8')


for file in os.listdir(file_path):
    if file.endswith('.nrrd'):
        print(file)

        data, header = nrrd.read(os.path.join(file_path, file))
        print(data.shape)
        with tiff.TiffWriter(os.path.join(file_path, file), imagej=True) as tifw:
            tifw.write(data.astype('uint8'), metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})

        # print('Enhancing contrast.....')
        # # _8bit_image = convert_to_8bit(data)
        # CE_image = ce(data)
        # print(f'Creating file {file} as tif ...')
        # print(CE_image)

# for item in os.listdir(file_path):
#     if item.endswith(".tif"):
#
#         # ****Contrast Enhancement, 8bit conversion, image processing with CV techniques******#
#         g = tiff.imread(os.path.join(file_path, item))
#         print(f'Image stack to be rotated: {item}')
#         theta = float(input('Enter the angle by which image to be rotated:'))
#
#
#         rotated_image = tiff_unstackAndrestack(os.path.join(file_path, item))
#         print(f'Creating Post-Processed Image: Processed_{item}')

