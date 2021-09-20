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
import cv2 as cv
import numpy as np
import tifffile as tiff
import SimpleITK as sitk
from scipy import ndimage
file_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data\aligned\ccka_4'


def image_to_tiff(image):
    print(f'Creating file {name}.tif')
    # metadata={'spacing': ['1./VoxelSizeList[0]', '1./VoxelSizeList[0]', '1'], 'unit': 'um',
    #                                   'axes ': 'ZYX', 'imagej': 'True'}
    return tiff.imwrite(os.path.join(file_path, f"{name}.tif"), image)


def contrast_enhancement(f):
    alpha = 3.0  # Contrast control (1.0-3.0) but 3 is required for my purposes here
    beta = 1  # Brightness control (0-100). Not to be added beyond 5, to not hamper the signal with salt and pepper
    # noise.
    contrast_enhanced_image = cv.convertScaleAbs(f, alpha=alpha, beta=beta)
    return contrast_enhanced_image.astype('uint8')


def split_and_rename(f):
    filename, exte = f.split('.')
    return filename


for file in os.listdir(file_path):
    if file.endswith('.nrrd'):
        print(file)
        processed_page_list = []
        name = split_and_rename(file)
        aligned_image = sitk.ReadImage(os.path.join(file_path, file))
        aligned_image_array_list = list(sitk.GetArrayFromImage(aligned_image))
        # we now have a list of 2D images and I can do processing on them and then restack them.

        for image in aligned_image_array_list:
            ce_image = contrast_enhancement(image)
            min_filter_image = ndimage.minimum_filter(ce_image, size=1)
            # filtered_image1 = cv.medianBlur(ce_image, 1)
            filtered_image = cv.bilateralFilter(min_filter_image.astype('uint8'), 9, 75, 75)
            processed_page_list.append(filtered_image)

        processed_image_stack = np.stack(processed_page_list)
        processed_tiff_image = image_to_tiff(processed_image_stack)
