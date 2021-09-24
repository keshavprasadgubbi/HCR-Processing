USER = "ekuehn"
# date = input("Enter line name of the fish: ")
# # base_fish_num = input("Enter base fish number you have chosen: ")
# tag = input("Enter the tag name for the fish line:")

L6 = ["#SBATCH -o /raven/u/ekuehn/outputs/tjob_hybrid_out.%j \n",
      "#SBATCH -e /raven/u/ekuehn/outputs/tjob_hybrid_err.%j \n"]
L7 = ["#SBATCH -D /raven/u/ekuehn \n", "# Job name: \n", "#SBATCH -J alignment \n",
      "# Number of nodes and MPI tasks per node: \n", "#SBATCH --nodes=1 \n", "#SBATCH --ntasks-per-node=1 \n",
      "# for OpenMP: \n", "#SBATCH --cpus-per-task=36\n", "# \n"]
L8 = ["#SBATCH --mem=120000 \n", "#SBATCH --mail-type=none \n", "#SBATCH --mail-user=ekuehn@neuro.mpg.de \n",
      "# Wall clock limit: \n", "#SBATCH --time=24:00:00 \n", "export OMP_NUM_THREADS=36 \n",
      "# For pinning threads correctly: \n", "export OMP_PLACES=cores \n", " \n"]
L9 = ["antsbin=/u/ekuehn/ANTs/antsinstallExample/install/bin \n"]

output = ["/u/${USER}/HCR/${HCR}/T_${HCR}_ \n",
          "output2=/u/${USER}/HCR/${HCR}/T_gcamp_${HCR}.nrrd \n",
          "output3=/u/${USER}/HCR/${HCR}/T_${ch2}.nrrd \n",
          "output4=/u/${USER}/HCR/${HCR}/T_${ch3}.nrrd \n"]

input = ["input1=/u/${USER}/HCR/${HCR}/${HCR}_ch1_gcamp.nrrd \n",
         "input2=/u/${USER}/HCR/${HCR}/${HCR}_ch2_${ch2}.nrrd \n",
         "input3=/u/${USER}/HCR/${HCR}/${HCR}_ch3_${ch3}.nrrd \n",
         "template=/u/${USER}/HCR/refbrain/final_HCR_standard_atlas_space.nrrd \n"]

L10 = ["srun $antsbin/antsRegistration -d 3 \ \n", "--float 1 \ \n",
      "-o [${output1},${output2}] \ \n", "--interpolation WelchWindowedSinc \ \n", "--use-histogram-matching 0 \ \n",
      "-r [${template1},${input1},1] \ \n", "-t rigid[0.1] \ \n", "-m MI[${template},${input1},1,32,Regular,0.25] \ \n",
      "-c [200x200x200x0,1e-8,10] \ \n", "--shrink-factors 12x8x4x2 \n", "--smoothing-sigmas 4x3x2x1vox \ \n",
      "-t Affine[0.1] \ \n", "-m MI[${template},${input1},1,32,Regular,0.25] \ \n", "-c [200x200x200x0,1e-8,10] \ \n",
      "--shrink-factors 12x8x4x2  \ \n", "--smoothing-sigmas 4x3x2x1 \ \n", "-t SyN[0.1,6,0.0] \ \n",
      "-m CC[${template},${input1},1,2] \n", "-c [200x200x200x200x10,1e-7,10] \ \n",
      "--shrink-factors 12x8x4x2x1 \ \n", "--smoothing-sigmas 4x3x2x1x0 \n"]


L11 = ["$antsbin/antsApplyTransforms -d 3 \ \n", "-v 0 \ \n", "-- float \ \n", "-n WelchWindowedSinc \ \n",
       "-i ${input2} \ \n", "-r ${template} \ \n", "-o ${output3} \ \n", "-t ${output1}1Warp.nii.gz \ \n",
       "-t ${output1}0GenericAffine.mat \n", " \n"]

L12 = ["$antsbin/antsApplyTransforms -d 3 \ \n", "-v 0 \ \n", "-- float \ \n", "-n WelchWindowedSinc \ \n",
       "-i ${input2} \ \n", "-r ${template} \ \n", "-o ${output3} \ \n", "-t ${output1}1Warp.nii.gz \ \n",
       "-t ${output1}0GenericAffine.mat \n", " \n"]


def create_script(output_path, channellist, username):
    file2 = open(rf"C:\Users\keshavgubbi\Desktop\HCR\HCR_alignment_line.sh", "w")
    file2.write("#!/bin/bash -l \n")
    file2.write("# Standard output and error: \n")
    file2.writelines(L6)
    file2.write("# Initial working directory: \n")
    file2.writelines(L7)
    file2.write("# Request 128 GB of main Memory per node in Units of MB: \n")
    file2.writelines(L8)
    file2.write(f"HCR= \n")
    file2.write(f"ch2= \n")
    file2.write(f"ch3= \n")
    file2.write("\n")
    file2.writelines(L9)
    file2.write("\n")
    file2.writelines(output)
    file2.write("\n")
    file2.writelines(input)
    file2.write("\n")
    file2.write("\n")
    file2.write("\n")
    file2.write("#Run the ANTs Program: \n")
    file2.writelines(L10)
    file2.write("\n")
    file2.writelines(L11)
    file2.write("\n")
    file2.writelines(L12)
    file2.close()  # to change file access modes
    return file2

if __name__ == '__main__':
    create_script()




