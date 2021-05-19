# *** Author: Keshava Prasad Gubbi***
# Script for postprocessing Inbal's HCR Lines.

# DONE: Read the aligned .nrrd 32 bit image files after downloading from the cluster, with index order C
# DONE: Convert to 8bit image
# DONE: Enhance contrast on the array
# DONE: write the respective array stack into a tiff file stack.
# DONE: Read the tiff image and unstack page by page and do image processing and restack it
# DONE: Gaussian Filtering/Bilateral Filtering in the array stack.
# DONE: sharpen the image via minimum 3D filter/other sharpening tools.
# DONE: Rewrite the respective array stack into a tiff file stack.
# DONE: Loop over the z dim of the image stack and finish the processing and later restack again


import os
from skimage import exposure
from skimage.filters.rank import mean_bilateral
from skimage.morphology import disk
import numpy as np
import tifffile as tiff
import SimpleITK as sitk
from scipy import ndimage
file_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data\aligned\ccka_4'


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

def split_and_rename(f):
    filename, exte = f.split('.')
    return filename


processed_page_list = []
for file in os.listdir(file_path):
    if file.endswith('.nrrd'):
        print(file)
        name = split_and_rename(file)
        aligned_image = sitk.ReadImage(os.path.join(file_path, file))
        aligned_image_array_list = list(sitk.GetArrayFromImage(aligned_image))
        # we now have a list of 2D images and I can do processing on them and then restack them.
        print(len(aligned_image_array_list))
        for image in aligned_image_array_list:
            print(image.shape)
            ce_image = ce(image)
            bilat_img = mean_bilateral(ce_image, disk(20), s0=10, s1=10)
            min_filter_image = ndimage.minimum_filter(bilat_img, size=10)
            processed_page_list.append(min_filter_image)
        # print(len(processed_page_list))
        processed_image_stack = np.stack(processed_page_list)
        # print('processed_image_stack')
        # print(processed_image_stack.shape)
        # print(len(processed_image_stack))

        print(f'Writing image {name}.tif')
        with tiff.TiffWriter(os.path.join(file_path, f"{name}.tif"), imagej=True) as tifw:
            tifw.write(processed_image_stack.astype('uint8'), metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})

