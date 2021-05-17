# *** Author: Keshava Prasad Gubbi***
# Script for postprocessing Inbal's HCR Lines.

# DONE: Read the aligned .nrrd 32 bit image files after downloading from the cluster, with index order C
#TODO: Loop over the z dim of the image stack and finish the processing and later restack again.
# TODO: Convert to 8bit image
# TODO: Enhance contrast on the array
# TODO: Gaussian Filtering/Bilateral Filtering in the array stack.
# TODO: sharpen the image via minimum 3D filter/other sharpening tools.
# TODO: Rewrite the respective array stack into a tiff file stack.

import os
import nrrd
from skimage import io, exposure, filters

file_path = r'C:\Users\keshavgubbi\Desktop\HCR\raw_data'


def ce(f):
    # i = img_as_float(io.imread(f)).astype(np.float64)
    logarithmic_corrected = exposure.adjust_log(f, 1)
    return logarithmic_corrected


for file in os.listdir(file_path):
    if file.endswith('.nrrd'):
        print(file)

        data, header = nrrd.read(os.path.join(file_path, file))
        print(data.shape)
        print(header)
        # print(aligned_image.dtype)
        # print(f"The file {aligned_image} has dimensions : {aligned_image.shape} and is of type: {aligned_image.dtype} ")


